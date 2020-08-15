from pathlib import Path

from ndl_tools.formatter import Formatter


def test_formatter():
    with (Path(".data") / "diff.html").open("rt") as fp:
        diff_html = fp.read()
        print()
    Formatter.format(diff_html)
