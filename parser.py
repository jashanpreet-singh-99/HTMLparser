import os
import numpy as np
import pandas as pd

"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

"""Tags without closing tag."""
SINGLETON_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
                  'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

"""Text only tags"""
TEXT_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title', 'label', 'p', 'a']


IS_TAG = False
IS_MISC = False
IS_COMMENT = False

IS_ATTRIBUTES = False
IS_ATTRIBUTE_VALUE = False

IS_CLOSING = False

IS_TAG_INSIDE = False

TAG_STACK = []

TAG_ATTRIBUTES = {}

comment_close = ''
comment_count = 0

tag = ''
doctype = ''
comment = ''
attribute = ''
attribute_value = ''
attribute_closer = ''
attribute_special_char = []

tag_inside_value = ''

open_tag_closer = ''

"""Create the base index table."""
HTML_INDEX = pd.DataFrame()

"""HTML_INDEX save location."""
HTML_INDEX_DIR = os.path.join(os.getcwd(), "html_index.csv")


def process_address_from_stack():
    """ Convert the current TAG_STACK to address for faster identification of \
    coding block while searching.
    """
    address = '||'.join(TAG_STACK)
    return address


def save_attributes_into_db(dict_data):
    global HTML_INDEX
    path = process_address_from_stack()
    dict_data['path'] = path
    db_entry = pd.DataFrame([dict_data])
    HTML_INDEX = HTML_INDEX.append(db_entry)


def process_attribute(attribute, attribute_value):
    TAG_ATTRIBUTES[attribute] = attribute_value


for ch in data:
    if IS_ATTRIBUTES:
        if ch == '>':
            """Processing for ending tag in attribute value."""
            if len(attribute_special_char) > 0:
                attribute_value += ch
                continue
            if attribute_value[-1] == '/':
                attribute_value = attribute_value[:-1]
            attribute_value = attribute_value[1:-1]
            print("Attribute : ", attribute, " -> ", attribute_value)
            process_attribute(attribute, attribute_value)
            save_attributes_into_db(TAG_ATTRIBUTES)
            TAG_ATTRIBUTES = {}
            attribute = ''
            attribute_value = ''
            IS_ATTRIBUTES = False
            IS_ATTRIBUTE_VALUE = False
            if TAG_STACK[-1] in SINGLETON_TAGS:
                TAG_STACK.pop()
                print("REMOVE : ", TAG_STACK)
            else:
                if TAG_STACK[-1] in TEXT_TAGS:
                    IS_TAG_INSIDE = True
        elif IS_ATTRIBUTE_VALUE:
            if ch == ' ':
                """Space in the Attribute value, possibility of new attributes \
                or check if it is part of the attribute value.
                """
                if len(attribute_special_char) > 0:
                    attribute_value += ch
                    continue
                attribute_value = attribute_value[1:-1]
                print("Attribute : ", attribute, " -> ", attribute_value)
                process_attribute(attribute, attribute_value)
                IS_ATTRIBUTE_VALUE = False
                attribute = ''
                attribute_value = ''
            elif ch == '"':
                """Keep track of special char to pevent premature ending."""
                if len(attribute_special_char) == 0:
                    attribute_special_char.append('"')
                else:
                    attribute_special_char.pop()
                attribute_value += ch
            else:
                attribute_value += ch
        elif ch == '=':
            """Change from attribute to attribute value."""
            IS_ATTRIBUTE_VALUE = True
        else:
            attribute += ch
        continue
        # / IS_ATTRIBUTES
    if IS_COMMENT:
        """Process the ch as a comment value."""
        if ch == '-':
            if comment_count == 0:
                comment_count += 1
                continue
            comment_close += ch
            comment += ch
            continue
        elif ch == '>':
            """Determine the end of tag."""
            if comment_close == '--':
                comment = comment[:-2]
                IS_COMMENT = False
                print("Comment : ", comment)
                comment = ''
                comment_close = ''
                comment_count = 0
            else:
                comment += ch
            continue
        else:
            comment += ch
            if len(comment_close) > 0:
                comment_close = ''
            continue
        # / IS_COMMENT
    if IS_MISC:
        """Check for deciding whether its comment or DOCTYPE."""
        if ch == '-':
            IS_COMMENT = True
            IS_MISC = False
        elif ch == '>':
            IS_MISC = False
            print("doctype : ", doctype)
            doctype = ''
        else:
            doctype += ch
        continue
        # / IS_MISC
    if IS_TAG:
        """Check if the char is in tag or misc."""
        if ch == '!':
            IS_MISC = True
            IS_TAG = False
        elif ch == '/':
            """Declare that the last non singleton tag is closing."""
            IS_CLOSING = True
        else:
            if ch == ' ':
                """Declare the end of tag name and start of attributes."""
                TAG_STACK.append(tag)
                print("ADD : ", TAG_STACK)
                tag = ''
                IS_ATTRIBUTES = True
                IS_TAG = False
            elif ch == '>':
                """The closing process of the last open non singleton tag."""
                if IS_CLOSING:
                    if TAG_STACK[-1] == tag:
                        print("REMOVE : ", TAG_STACK)
                        TAG_STACK.pop()
                        IS_CLOSING = False
                else:
                    """If the tag has no attributes and is still open."""
                    if tag not in SINGLETON_TAGS:
                        TAG_STACK.append(tag)
                        print("ADD : ", TAG_STACK)
                        if tag in TEXT_TAGS:
                            IS_TAG_INSIDE = True
                    else:
                        print("REMOVE : ", TAG_STACK)
                        TAG_STACK.pop()
                print(TAG_STACK)
                tag = ''
                IS_TAG = False
            else:
                tag += ch
        continue
        # IS_TAG
    if IS_TAG_INSIDE:
        if ch == '<':
            if len(open_tag_closer) == 0:
                open_tag_closer = ch
            tag_inside_value += ch
        elif ch == '/':
            if open_tag_closer == '<':
                open_tag_closer += ch
            tag_inside_value += ch
        elif ch == '!':
            tag_inside_value += ch
        elif ch == '-':
            if len(open_tag_closer) == 1:
                IS_COMMENT = True
                open_tag_closer = ''
                tag_inside_value = tag_inside_value[:-2]
            else:
                tag_inside_value += ch
        else:
            if open_tag_closer == '</' and ch == TAG_STACK[-1][0]:
                """The open tag is closing."""
                tag_inside_value = tag_inside_value[:-2]
                print("TAG INSIDE VALUE : ", tag_inside_value)
                IS_CLOSING = True
                IS_TAG = True
                IS_TAG_INSIDE = False
                tag_inside_value = ''
                tag = ch
            else:
                tag_inside_value += ch
                if len(open_tag_closer) > 0:
                    open_tag_closer = ''
        continue
        # / IS_TAG_INSIDE
    if ch == '<':
        """Declare starting of a tag related process."""
        IS_TAG = True
        continue
        # / '<'

print(HTML_INDEX.columns)
HTML_INDEX.to_csv(HTML_INDEX_DIR)
