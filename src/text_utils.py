import re
from src.HTMLAttributeParser import HTMLAttributeParser


def extract_attributes(html_element):
    """Given a string for an HTML element such as
    <el
         a="foo" B="bar" c="&98;az" d=boz
         empty= noval entity="&amp;"
         sq='"' dq="'"
    >
    Decode and return a dictionary of attributes.
    {
        'a': 'foo', 'b': 'bar', c: 'baz', d: 'boz',
        'empty': '', 'noval': None, 'entity': '&',
        'sq': '"', 'dq': '\''
    }.
    NB HTMLParser is stricter in Python 2.6 & 3.2 than in later versions,
    but the cases in the unit test will work for all of 2.6, 2.7, 3.2-3.5.
    """
    parser = HTMLAttributeParser()
    try:
        parser.feed(html_element)
        parser.close()
    except Exception:  # pylint: disable=W
        pass
    return parser.attrs


def hidden_inputs(html):
    html = re.sub(r"<!--(?:(?!<!--).)*-->", "", html)
    hidden_inputs = {}  # pylint: disable=W
    for entry in re.findall(r"(?i)(<input[^>]+>)", html):
        attrs = extract_attributes(entry)
        if not entry:
            continue
        if attrs.get("type") not in ("hidden", "submit"):
            continue
        name = attrs.get("name") or attrs.get("id")
        value = attrs.get("value")
        if name and value is not None:
            hidden_inputs[name] = value
    return hidden_inputs


def search_regex(pattern, string, name, default=object(), fatal=True, flags=0, group=None):
    """
    Perform a regex search on the given string, using a single or a list of
    patterns returning the first matching group.
    In case of failure return a default value or raise a WARNING or a
    RegexNotFoundError, depending on fatal, specifying the field name.
    """
    if isinstance(pattern, str):
        mobj = re.search(pattern, string, flags)
    else:
        for p in pattern:
            mobj = re.search(p, string, flags)
            if mobj:
                break

    _name = name

    if mobj:
        if group is None:
            # return the first matching group
            return next(g for g in mobj.groups() if g is not None)
        else:
            return mobj.group(group)
    elif default is not object():
        return default
    elif fatal:
        print("[-] Unable to extract %s" % _name)
        exit(0)
    else:
        print("[-] unable to extract %s" % _name)
        exit(0)
