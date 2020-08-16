"""
Quick hack to see what it will take to format the HTML output from the difflib.html_diff() into
plain text that can be displayed in pytest.
"""
from html.parser import HTMLParser

ADD_FORMAT_ON = "\033[0;32m"
SUB_FORMAT_ON = "\033[0:31m"
FORMAT_OFF = "\033[0m"


class Row:
    def __init__(self):
        self.data = list()

    def add(self, data: str):
        self.data.append(data.replace("\xa0", " ") if data else data)

    def finalize(self):
        l = self.data[2] if self.data[2] else ""
        r = self.data[5] if self.data[5] else ""
        print(f"{l:12} {r:12}")


class Formatter(HTMLParser):
    def __init__(self):
        self.in_table = False
        self.done = False
        self.row = None
        self.looking_for_data = False
        self.data = None
        self.change_mark = None
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "tbody" and not self.done:
            self.in_table = True
            return
        if self.in_table and tag == "tr":
            self.row = Row()
        if self.in_table and tag == "td":
            self.looking_for_data = True
            self.data = None
        if self.looking_for_data and tag == "span":
            class_attr = [value for attr, value in attrs if attr == "class"][0]
            if class_attr == "diff_add":
                self.change_mark = ADD_FORMAT_ON
            elif class_attr == "diff_sub":
                self.change_mark = SUB_FORMAT_ON
            else:
                raise ValueError(class_attr)
            self.data = "".join([self.data, self.change_mark]) if self.data else self.change_mark

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_table = False
            return
        if self.in_table and tag == "tr":
            self.row.finalize()
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

    @staticmethod
    def format(diff: str):
        parser = Formatter()
        parser.feed(diff)
