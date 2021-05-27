import os

"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

"""Attribute without."""
SINGLETON_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
                  'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

IS_TAG = False
IS_MISC = False
IS_COMMENT = False

IS_ATTRIBUTES = False
IS_ATTRIBUTE_VALUE = False

IS_CLOSING = False

TAG_STACK = []

ID = {}
CLASS = {}

comment_close = ''

tag = ''
doctype = ''
comment = ''
attribute = ''
attribute_value = ''
attribute_closer = ''
attribute_special_char = []


def process_address_from_stack():
    """ Convert the current TAG_STACK to address for faster identification of \
    coding block while searching.
    """
    address = '||'.join(TAG_STACK)
    return address


def process_attribute(attribute, attribute_value):
    if attribute == 'id':
        """ store the address of each id element.

        the address can be same for 2 or more elements, hence a check is \
        implemented later on while fetching the data.
        """
        ID[attribute_value] = process_address_from_stack()
    elif attribute == 'class':
        """ store the addresses of all class elements.

        the address can be same for 2 or more elements, hence a check is \
        implemented later on while fetching the data.
        """
        if attribute_value in CLASS.keys():
            CLASS[attribute_value].append(process_address_from_stack())
        else:
            CLASS[attribute_value] = [process_address_from_stack()]


for ch in data:
    if IS_ATTRIBUTES:
        if ch == '>':
            """Processing for ending tag in attribute value."""
            if attribute_value[-1] == '/':
                attribute_value = attribute_value[:-1]
            attribute_value = attribute_value[1:-1]
            print("Attribute : ", attribute, " -> ", attribute_value)
            process_attribute(attribute, attribute_value)
            attribute = ''
            attribute_value = ''
            IS_ATTRIBUTES = False
            IS_ATTRIBUTE_VALUE = False
            if TAG_STACK[-1] in SINGLETON_TAGS:
                TAG_STACK.pop()
                print("REMOVE : ", TAG_STACK)
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
            if len(comment) == 0:
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
                        print("Closing opened tag : ", tag)
                        TAG_STACK.pop()
                        IS_CLOSING = False
                else:
                    """If the tag has no attributes and is still open."""
                    if tag not in SINGLETON_TAGS:
                        TAG_STACK.append(tag)
                        print("ADD : ", TAG_STACK)
                    else:
                        TAG_STACK.pop()
                print(TAG_STACK)
                tag = ''
                IS_TAG = False
            else:
                tag += ch
        continue
        # IS_TAG
    if ch == '<':
        """Declare starting of a tag related process."""
        IS_TAG = True
        continue
        # / '<'

print(ID)
print(CLASS)
