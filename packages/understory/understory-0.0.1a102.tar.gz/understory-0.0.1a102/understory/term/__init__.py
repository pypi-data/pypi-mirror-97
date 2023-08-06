"""Tools for a metamodern terminal environment."""

# TODO framework (argparse/argcomplete, ncurses) & agent (sh) like `web`
# TODO dotdir config files
# TODO pager w/ hjkl, [shift+]space, ctrl+[b|f], tab through links (web/mail),
#      mouse scroll & click on links

import builtins
import re
import os
import sys
import textwrap

from .cli import Application as application  # noqa

__all__ = ["application", "print", "get_output_width", "get_dimensions",
           "wraptext"]


ESCAPE = "\x1b[{}m"
RESET = ESCAPE.format(0)
colors = "ergybmcwt"  # grey red green yellow blue magenta cyan white & reset
attributes = "ldiuborcs"  # lght drk itlc under blnk over rev conceal & strike

_print = print


def wrap(text, indent=0):
    joiner = "\n" + (" " * indent)
    return joiner.join(textwrap.wrap(text, get_output_width() + indent))


def print(*values, sep=" ", end="\n", **kwargs):
    """Enhanced print with color and logging."""
    # TODO log file, stdout, stderr via `kwargs["file"]` -- jive w/ supervisor
    pattern = r"/(X|([ldiuborcsLDIUBORCS]+,)?" \
              r"(L?[ERGYBMCWT]?)?(l?[ergybmcwt]?)?)/"

    colors_off = os.environ.get("COLORS_OFF")

    def repl(matchobj):
        full_code, attribute_codes, background, foreground = matchobj.groups()
        if not any(matchobj.groups()):
            return "//"  # don't clobber consecutive slashes; e.g. http://...
        if full_code == "l":  # TODO handle false positives more reliably
            return "/{}/".format(full_code)
        if colors_off:
            return ""
        if not sys.stdout.isatty() and not os.environ.get("COLORS_ON"):
            return ""
        if full_code == "X":
            return RESET
        codes = []
        if attribute_codes:
            for attribute_code in attribute_codes.rstrip(","):
                attribute_offset = (20 if attribute_code.isupper() else 0)
                z = [attr[0] for attr in
                     attributes].index(attribute_code.lower()) + 1
                codes.append(attribute_offset + z)
        if background:
            codes.append((100 if background.startswith("L") else 40)
                         + colors.index(background.lower()[-1]))
        if foreground:
            codes.append((90 if foreground.startswith("l") else 30)
                         + colors.index(foreground[-1]))
        return ESCAPE.format(";".join(map(str, codes)))

    def colorize(text):
        text = re.sub(pattern, repl, str(text))
        if not colors_off:
            text += RESET
        return text

    _print(*map(colorize, values), sep=colorize(sep), end=colorize(end),
           **kwargs)


builtins.print = print  # NOTE overriding print()


def get_output_width():
    """Return the best of env var `TTY_WIDTH`, current terminal width or 80."""
    return int(os.environ.get("TTY_WIDTH", get_dimensions()[1]))


def get_dimensions():
    """Return a 2-tuple of terminal's height and width."""
    from fcntl import ioctl
    from termios import TIOCGWINSZ
    from struct import pack, unpack
    return unpack("HHHH", ioctl(0, TIOCGWINSZ, pack("HHHH", 0, 0, 0, 0)))[:2]
