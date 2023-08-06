import sys
import json
import html
from bs4 import BeautifulSoup

BOOKMARK_FILE_START_SEQUENCE = """
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
"""


def make_folder(h3_tag, children):
    res = {}
    res["title"] = h3_tag.text
    res["type"] = "folder"
    for key in ["add_date", "last_modified", "personal_toolbar_folder"]:
        res[key] = h3_tag.get(key)
    res["children"] = children
    return res


def make_item(a_tag):
    res = {}
    res["title"] = a_tag.text
    res["type"] = "item"
    for key in ["add_date", "bookmark", "href", "icon"]:
        res[key] = a_tag.get(key)
    return res


def process_node(node):
    if node.name == "dl":
        # Process folder
        return [process_node(child) for child in node.findChildren(recursive=False) if child.name == "dt"]  # noqa: E501
    if node.name == "dt":
        # Process folder OR link
        for child in node.findChildren(recursive=False):
            if child.name == "a":
                return make_item(child)
            if child.name == "h3":
                children = process_node(child.find_next_sibling("dl"))
                return make_folder(child, children)


def serialize_to_html(bookmarks):

    def fmt_tag_values(d, keys):
        res = ""
        for k in keys:
            if d[k]:
                res += ' %s="%s"' % (k.upper(), d[k])
        return res

    def _serialize_to_html(bookmarks, level):
        res = ""
        for bookmark in bookmarks:
            indent = " " * level * 4
            # Folder
            if bookmark["type"] == "folder":
                attrs = fmt_tag_values(bookmark, ["add_date", "last_modified",
                                                  "personal_toolbar_folder"])
                line = ("""<DT><H3%s>%s</H3>"""
                        % (attrs, html.escape(bookmark["title"])))
                res += indent + line + "\n"
                res += indent + "<DL><p>\n"
                res += _serialize_to_html(bookmark["children"], level+1)
                res += indent + "</DL><p>\n"
            # Item
            if bookmark["type"] == "item":
                line = ("""<DT><A%s>%s</A>""" %
                        (fmt_tag_values(bookmark, ["href", "add_date", "icon"]),
                         html.escape(bookmark["title"])))
                res += indent + line + "\n"
        return res

    res = BOOKMARK_FILE_START_SEQUENCE
    res += _serialize_to_html(bookmarks, 1)
    res += "</DL><p>"
    return res


def dump_chrome(bookmarks, f):
    f.write(serialize_to_html(bookmarks))


def load_chrome(bytes):
    soup = BeautifulSoup(bytes, "html5lib")
    bookmarks = process_node(soup.find_all("dl")[0])
    return bookmarks
