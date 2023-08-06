"""The command line utility for ChromaTerm"""
import argparse
import os
import re
import select
import signal
import sys

import yaml

from chromaterm import Color, Config, Rule
from chromaterm.default_config import write_default_config

# A couple of sections of the program are used _rarely_ and I don't want to
# _always_ spend time importing them.
# pylint: disable=import-outside-toplevel

# Maximum chuck size per read
READ_SIZE = 4096  # 4 KiB

# CT cannot determine if it is processing input faster than the piping process
# is outputting or if the input has finished. To work around this, CT will wait
# a bit prior to assuming there's no more data in the buffer. There's no impact
# on performance as the wait is cancelled if read_fd becomes ready. 1/256 is
# smaller (shorter) than the fastest key repeat (1/255 second).
WAIT_FOR_SPLIT = 1 / 256

# Sequences upon which ct will split during processing. This includes new lines,
# vertical spaces, form feeds, C1 set (ECMA-048), SCS (G0 through G3 sets),
# CSI (excluding SGR), and OSC.
SPLIT_RE = re.compile(r'(\r\n?|\n|\v|\f|\x1b[\x40-\x5a\x5c\x5e\x5f]|'
                      r'\x1b[\x28-\x2b\x2d-\x2f][\x20-\x7e]|'
                      r'\x1b\x5b[\x30-\x3f]*[\x20-\x2f]*[\x40-\x6c\x6e-\x7e]|'
                      r'\x1b\x5d[\x08-\x0d\x20-\x7e]*(?:\x07|\x1b\x5c))')


def args_init(args=None):
    """Returns the parsed arguments (an instance of argparse.Namespace).

    Args:
        args (list): A list of program arguments, Defaults to sys.argv.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('program',
                        type=str,
                        metavar='program ...',
                        nargs='?',
                        help='run a program with anything after it used as '
                        'arguments')

    parser.add_argument('arguments',
                        type=str,
                        nargs=argparse.REMAINDER,
                        help=argparse.SUPPRESS,
                        default=[])

    parser.add_argument('--config',
                        metavar='FILE',
                        type=str,
                        help='location of config file (default: %(default)s)',
                        default='$HOME/.chromaterm.yml')

    parser.add_argument('--reload',
                        action='store_true',
                        help='Reload the config of all CT instances')

    parser.add_argument('--rgb',
                        action='store_true',
                        help='Use RGB colors (default: detect support, '
                        'fallback to xterm-256)',
                        default=None)

    return parser.parse_args(args=args)


def eprint(*args, **kwargs):
    """Prints a message to stderr."""
    print(sys.argv[0] + ':', *args, file=sys.stderr, **kwargs)


def load_rules(config, data, rgb=False):
    """Reads rules from a YAML-based string, formatted like so:
    rules:
    - description: My first rule
        regex: Hello
        color: b#123123
    - description: My second rule is specfic to groups
        regex: W(or)ld
        color:
        0: f#321321
        1: bold

    Any errors are printed to stderr.

    Args:
        data (str): A string containg YAML data.
        rgb (bool): Whether the terminal is RGB-capable or not.
    """
    # Load the YAML configuration file
    try:
        data = yaml.safe_load(data) or {}
    except yaml.YAMLError as exception:
        eprint('Parse error:', exception)
        return

    rules = data.get('rules') if isinstance(data, dict) else None

    if not isinstance(rules, list):
        eprint('Parse error: "rules" is not a list')
        return

    # Clear existing rules
    for rule in config.rules:
        config.remove_rule(rule)

    for rule in rules:
        rule = parse_rule(rule, rgb=rgb)

        if isinstance(rule, Rule):
            config.add_rule(rule)
        else:
            eprint(rule)


def parse_rule(rule, rgb=False):
    """Returns an instance of chromaterm.Rule if parsed correctly. Otherwise, a
    string with the error message is returned. The rule is a dictionary formatted
    according to `chromaterm.cli.load_rules`.

    Args:
        rule (dict): A dictionary representing the rule.
    """
    if not isinstance(rule, dict):
        return 'Rule {} not a dictionary'.format(repr(rule))

    description = rule.get('description')
    regex = rule.get('regex')

    if description:
        rule_repr = 'Rule(regex={}, description={})'.format(
            repr(regex), repr(description))
    else:
        rule_repr = 'Rule(regex={})'.format(repr(regex))

    try:
        parsed_rule = Rule(regex, description=description)
    except TypeError as exception:
        return 'Error on {}: {}'.format(rule_repr, exception)
    except re.error as exception:
        return 'Error on {}: re.error: {}'.format(rule_repr, exception)

    color = rule.get('color')

    if isinstance(color, str):
        color = {0: color}
    elif not isinstance(color, dict):
        return 'Error on {}: color {} is not a string'.format(
            rule_repr, repr(color))

    try:
        for group in color:
            parsed_color = Color(color[group], rgb=rgb)
            parsed_rule.set_color(parsed_color, group=group)
    except (TypeError, ValueError) as exception:
        return 'Error on {}: {}'.format(rule_repr, exception)

    return parsed_rule


def process_input(config, data_fd, forward_fd=None, max_wait=None):
    """Processes input by reading from data_fd, highlighting it using config,
    then printing it to sys.stdout. If forward_fd is not None, any data it has
    will be written (forwarded) into data_fd.

    Args:
        config (chromaterm.Config): Used for highlighting the data.
        data_fd (int): File descriptor to be read and highlighted.
        forward_fd (int): File descriptor to forwarded into data_fd. This is used
            in conjunction with run_program. None indicates forwarding is not
            required.
        max_wait (float): The maximum time to wait with no data on either of the
            file descriptors. None will block until at least one ready to be read.
    """
    fds = [data_fd] if forward_fd is None else [data_fd, forward_fd]
    buffer = ''

    ready_fds = read_ready(*fds, timeout=max_wait)

    while ready_fds:
        # There's some data to forward to the spawned program
        if forward_fd in ready_fds:
            try:
                os.write(data_fd, os.read(forward_fd, READ_SIZE))
            except OSError:
                # Spawned program or stdin closed; don't forward anymore
                fds.remove(forward_fd)

        # Data to be highlighted was received
        if data_fd in ready_fds:
            try:
                data_read = os.read(data_fd, READ_SIZE)
            except OSError:
                data_read = b''

            buffer += data_read.decode(encoding='utf-8', errors='replace')

            # Buffer was processed empty and data fd hit EOF
            if not buffer:
                break

            splits = split_buffer(buffer)

            # Process splits except for the last one as it might've been cut off
            for data, separator in splits[:-1]:
                sys.stdout.write(config.highlight(data) + separator)

            # Data was read and there's more to come; wait before highlighting
            if data_read and read_ready(data_fd, timeout=WAIT_FOR_SPLIT):
                buffer = splits[-1][0] + splits[-1][1]
            # No data buffered; print last split
            else:
                # A single character indicates keyboard typing; don't highlight
                if len(splits[-1][0]) == 1:
                    leftover_data = splits[-1][0]
                else:
                    leftover_data = config.highlight(splits[-1][0])

                sys.stdout.write(leftover_data + splits[-1][1])
                buffer = ''

            # Flush as the last split might not end with a new line
            sys.stdout.flush()

        ready_fds = read_ready(*fds, timeout=max_wait)


def read_file(location):
    """Returns the contents of a file or None on error. The error is printed to
    stderr.

    Args:
        location (str): The location of the file to be read.
    """
    location = os.path.expandvars(location)

    if not os.access(location, os.F_OK):
        eprint('Configuration file', location, 'not found')
        return None

    try:
        with open(location, 'r') as file:
            return file.read()
    except PermissionError:
        eprint('Cannot read configuration file', location, '(permission)')
        return None


def read_ready(*read_fds, timeout=None):
    """Returns a list of file descriptors that are ready to be read.

    Args:
        *read_fds (int): Integers that refer to the file descriptors.
        timeout (float): A timeout before returning an empty list if no file
            descriptor is ready. None waits until at least one file descriptor
            is ready.
    """
    return [] if not read_fds else select.select(read_fds, [], [], timeout)[0]


def reload_chromaterm_instances():
    """Reloads other ChromaTerm CLI instances by sending them signal.SIGUSR1.

    Returns:
        The number of processes reloaded.
    """
    import psutil

    count = 0
    current_process = psutil.Process()

    for process in psutil.process_iter():
        if process.pid == current_process.pid:  # Skip the current process
            continue

        try:
            # Only compare the first two arguments (Python and script paths)
            if process.cmdline()[:2] == current_process.cmdline()[:2]:
                os.kill(process.pid, signal.SIGUSR1)
                count += 1
        # As per the documentation, expect those errors when accessing the
        # methods of a process
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

    return count


def run_program(program_args):
    """Spawns a program in a pty fork to emulate a controlling terminal.

    Args:
        program_args (list): A list of program arguments. The first argument is
            the program name/location.

    Returns:
        A file descriptor (int) of the mater end of the pty fork.
    """
    import atexit
    import fcntl
    import termios
    import pty
    import shutil
    import struct
    import tty

    # Save the current tty's window size and attributes (used by slave pty)
    window_size = shutil.get_terminal_size()
    window_size = struct.pack('2H', window_size.lines, window_size.columns)

    try:
        attributes = termios.tcgetattr(sys.stdin.fileno())

        # Set to raw as the pty will be handling any processing
        tty.setraw(sys.stdin.fileno())
        atexit.register(termios.tcsetattr, sys.stdin.fileno(), termios.TCSANOW,
                        attributes)
    except termios.error:
        attributes = None

    # openpty, login_tty, then fork
    pid, master_fd = pty.fork()

    if pid == 0:
        # Update the slave's pty (now on std fds) window size and attributes
        fcntl.ioctl(sys.stdin.fileno(), termios.TIOCSWINSZ, window_size)

        if attributes:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, attributes)

        try:
            os.execvp(program_args[0], program_args)
        except FileNotFoundError:
            eprint(program_args[0] + ': command not found')

        # exec replaces the fork's process; only hit on exception
        sys.exit(1)
    else:
        return master_fd


def split_buffer(buffer):
    """Returns a tuples of tuples in the format of (data, separator). data should
    be highlighted while separator should be printed unchanged, after data.

    Args:
        buffer (str): A string to split using SPLIT_RE.
    """
    splits = SPLIT_RE.split(buffer)

    # Append an empty separator in case of no splits or no separator at the end
    splits.append('')

    # Group all splits into format of (data, separator)
    return tuple(zip(splits[0::2], splits[1::2]))


def main(args=None, max_wait=None, write_default=True):
    """Command line utility entry point.

    Args:
        args (list): A list of program arguments. Defaults to sys.argv.
        max_wait (float): The maximum time to wait with no data. None will block
            until data is ready to be read.
        write_default (bool): Whether to write the default configuration or not.
            Only written if it doesn't exist already.

    Returns:
        A string indicating status/error. Otherwise, returns None. It is meant to
        be used as sys.exit(chromaterm.cli.main()).
    """
    args = args_init(args)

    if args.reload:
        return 'Processes reloaded: ' + str(reload_chromaterm_instances())

    if write_default:
        # Write default config if not there
        write_default_config()

    config = Config()

    # Create the signal handler to trigger reloading the config
    def reload_config_handler(*_):
        load_rules(config, read_file(args.config) or '', rgb=args.rgb)

    # Trigger the initial loading
    reload_config_handler()

    if args.program:
        # ChromaTerm is spawning the program in a controlling terminal; stdin is
        # being forwarded to the program
        data_fd = run_program([args.program] + args.arguments)
        forward_fd = sys.stdin.fileno()
    else:
        # Data is being piped into ChromaTerm's stdin; no forwarding needed
        data_fd = sys.stdin.fileno()
        forward_fd = None

    # Ignore SIGPIPE (broken pipe) and SIGINT (CTRL+C), and attach reload handler
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGUSR1, reload_config_handler)

    # Begin processing the data (blocking operation)
    process_input(config, data_fd, forward_fd=forward_fd, max_wait=max_wait)

    return None


if __name__ == '__main__':
    sys.exit(main())
