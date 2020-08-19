"""
Quick hack to see what it will take to format the HTML output from the difflib.html_diff() into
plain text that can be displayed in pytest.
"""
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional

ADD_FORMAT_ON = "\033[0;32m"
SUB_FORMAT_ON = "\033[0:31m"
CHANGE_FORMAT_ON = "\033[0:33m"
FORMAT_OFF = "\033[0m"
FORMAT_EXTRA_CHARS = len(ADD_FORMAT_ON) + len(FORMAT_OFF)

# ToDo: data really needs to be passed as a list.  Then the process of picking off enough charactors
#       to format to the correct width will be easier.   It will also allow for the correct
#       format off character to be added if needed.


class Row:
    def __init__(self, max_col_width: int):
        self.max_col_width = max_col_width
        self.data = list()

    def add(self, data: str):
        self.data.append(data.replace("\xa0", " ") if data else data)

    def finalize(self):
        left = self.data[2] if self.data[2] else ""
        right = self.data[5] if self.data[5] else ""

        left_chars = self.max_col_width + FORMAT_EXTRA_CHARS if FORMAT_OFF in left else self.max_col_width
        right_chars = self.max_col_width + FORMAT_EXTRA_CHARS if FORMAT_OFF in right else self.max_col_width

        return f"{left:{left_chars}} {right:{right_chars}}"


class Formatter(HTMLParser):
    def __init__(self, max_col_width: Optional[int] = 20):
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
            # ToDo: Get this into a mapping
            if class_attr == "diff_add":
                self.match = False
                self.change_mark = ADD_FORMAT_ON
            elif class_attr == "diff_sub":
                self.match = False
                self.change_mark = SUB_FORMAT_ON
            elif class_attr == "diff_chg":
                self.match = False
                self.change_mark = CHANGE_FORMAT_ON
            else:
                raise ValueError(class_attr)
            self.data = "".join([self.data, self.change_mark]) if self.data else self.change_mark

    def handle_endtag(self, tag):
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
            self.data = "".join([self.data, FORMAT_OFF]) if self.data else self.change_mark

    def handle_data(self, data):
        if self.looking_for_data:
            self.data = "".join([self.data, data]) if self.data else data

    def format(self, diff: str):
        with Path(".data/diff.html").open("wt") as fp:
            fp.write(diff)
        self.feed(diff)
        return self.match, "\n".join(self.output)
