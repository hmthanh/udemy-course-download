from abc import ABC
from html.parser import HTMLParser as compat_HTMLParser


# Thanks to a great open source utility youtube-dl ..
class HTMLAttributeParser(compat_HTMLParser, ABC):  # pylint: disable=W
    """Trivial HTML parser to gather the attributes for a single element"""

    def __init__(self):
        self.attrs = {}
        compat_HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)
