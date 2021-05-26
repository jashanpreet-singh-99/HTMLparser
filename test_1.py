import os

"""
Read the example file.
"""
EXAMPLE_FILE = os.path.join(os.getcwd(), "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

SINGLETON_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
                  'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

IS_TAG = False
IS_MISC = False
IS_COMMENT = False

IS_ATTRIBUTES = False
IS_ATTRIBUTE_VALUE = False

IS_CLOSING = False

TAG_STACK = []
comment_close = ''


tag = ''
doctype = ''
comment = ''
attribute = ''
attribute_value = ''
attribute_closer = ''
attribute_special_char = []

for ch in data:
    if IS_ATTRIBUTES:
        if ch == '/':
            if IS_ATTRIBUTE_VALUE:
                attribute_value += ch
        elif ch == '>':
            if attribute_value[-1] == '/':
                attribute_value = attribute_value[:-1]
            print("Attribute : ", attribute, " -> ", attribute_value[1:-1])
            attribute = ''
            attribute_value = ''
            IS_ATTRIBUTES = False
            IS_ATTRIBUTE_VALUE = False
        elif IS_ATTRIBUTE_VALUE:
            if ch == ' ':
                if len(attribute_special_char) > 0:
                    attribute_value += ch
                    continue
                print("Attribute : ", attribute, " -> ", attribute_value[1:-1])
                IS_ATTRIBUTE_VALUE = False
                attribute = ''
                attribute_value = ''
            elif ch == '"':
                if len(attribute_special_char) == 0:
                    attribute_special_char.append('"')
                else:
                    attribute_special_char.pop()
                attribute_value += ch
            else:
                attribute_value += ch
        elif ch == '=':
            IS_ATTRIBUTE_VALUE = True
        else:
            attribute += ch
        continue
    if IS_COMMENT:
        if ch == '-':
            if len(comment) == 0:
                continue
            comment_close += ch
            comment += ch
            continue
        elif ch == '>':
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
    if IS_MISC:
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
    if IS_TAG:
        if ch == '!':
            IS_MISC = True
            IS_TAG = False
        elif ch == '/':
            IS_CLOSING = True
            # print("Closing tag.")
        else:
            if ch == ' ':
                TAG_STACK.append(tag)
                # print("tag name : ", tag)
                print(TAG_STACK)
                tag = ''
                IS_ATTRIBUTES = True
                IS_TAG = False
            elif ch == '>':
                if IS_CLOSING:
                    while TAG_STACK[-1] in SINGLETON_TAGS:
                        TAG_STACK.pop()
                    if TAG_STACK[-1] == tag:
                        print("Closing opened tag : ", tag)
                        TAG_STACK.pop()
                        IS_CLOSING = False
                else:
                    TAG_STACK.append(tag)
                    # print("tag name : ", tag)
                print(TAG_STACK)
                tag = ''
                IS_TAG = False
            else:
                tag += ch
        continue
    if ch == '<':
        IS_TAG = True
        continue
