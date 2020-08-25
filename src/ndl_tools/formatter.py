"""
Quick hack to see what it will take to format the HTML output from the difflib.html_diff() into
plain text that can be displayed in pytest.
"""
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

ADD_FORMAT_ON = "\033[0;32m"
SUB_FORMAT_ON = "\033[0:31m"
CHANGE_FORMAT_ON = "\033[0:34m"
START_MARKS = {
    "diff_add": ADD_FORMAT_ON,
    "diff_sub": SUB_FORMAT_ON,
    "diff_chg": CHANGE_FORMAT_ON,
}
FORMAT_OFF = "\033[0m"
FORMAT_EXTRA_CHARS = len(ADD_FORMAT_ON) + len(FORMAT_OFF)

# ToDo: data really needs to be passed as a list.  Then the process of picking off enough characters
#       to format to the correct width will be easier.   It will also allow for the correct
#       format off character to be added if needed.


class Row:
    """
    Collect up each of the columns in a list and then format them all together at the end.
    """

    def __init__(self, max_col_width: int):
        """
        Start a new row of output.

        :param max_col_width: Future support for truncating or smart selection of a portion of a line.
        """
        self.max_col_width = max_col_width
        self.data = list()

    def add(self, data: str):
        """Add the next column to the row."""
        self.data.append(data.replace("\xa0", " ") if data else data)

    def finalize(self):
        """Concatenate the line together with any coloring required.  Truncate to max columns."""
        left = self.data[2] if self.data[2] else ""
        right = self.data[5] if self.data[5] else ""

        left_chars = (
            self.max_col_width + FORMAT_EXTRA_CHARS
            if FORMAT_OFF in left
            else self.max_col_width
        )
        right_chars = (
            self.max_col_width + FORMAT_EXTRA_CHARS
            if FORMAT_OFF in right
            else self.max_col_width
        )

        return f"{left:{left_chars}} {right:{right_chars}}"


class Formatter(HTMLParser):
    def __init__(self, max_col_width: Optional[int] = 20):
        """
        Keep track of all the state variables for parsing each of the rows.

        :param max_col_width: Limit for how wide any line can be.
        """
        self.max_col_width = max_col_width
        self.in_table = False
        self.done = False
        self.row = None
        self.looking_for_data = False
        self.data = None
        self.change_mark = None
        self.output = list()
        self.match = True
        super().__init__()

    def handle_starttag(self, tag, attrs):
        """
        Process the start tags to change the state of the parser.
        """
        if tag == "tbody" and not self.done:
            self.in_table = True
            return
        if self.in_table and tag == "tr":
            self.row = Row(self.max_col_width)
        if self.in_table and tag == "td":
            self.looking_for_data = True
            self.data = None
        if self.looking_for_data and tag == "span":
            class_attr = [value for attr, value in attrs if attr == "class"][0]
            self.match = False
            self.change_mark = START_MARKS[class_attr]
            self.data = (
                "".join([self.data, self.change_mark])
                if self.data
                else self.change_mark
            )

    def handle_endtag(self, tag):
        """
        Process the end tags to change the state of the parser.
        """
        if tag == "tbody":
            self.in_table = False
            return
        if self.in_table and tag == "tr":
            self.output.append(self.row.finalize())
            self.row = None
        if self.in_table and tag == "td":
            self.row.add(self.data)
            self.looking_for_data = False
            self.data = None
        if self.looking_for_data and tag == "span":
            self.data = (
                "".join([self.data, FORMAT_OFF]) if self.data else self.change_mark
            )

    def handle_data(self, data):
        if self.looking_for_data:
            self.data = "".join([self.data, data]) if self.data else data

    def format(self, diff: str):
        """Parse and format the html into a colored test format."""
        self.feed(diff)
        return self.match, "\n".join(self.output)
