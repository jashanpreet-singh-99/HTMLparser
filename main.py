import re
import os
from automata import Automata

autoM = Automata()

open_tag = " "
close_tag = " "
doc_type = " "
comment = " "
attribute = " "
attribute_value = " "

tag_content = " "

SINGLE_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
                  'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

def add_open_tag(ch):
    global open_tag
    open_tag += ch


def close_single_tag(ch):
    print("Single_tag :", ch)

def add_close_tag(ch):
    global close_tag
    close_tag += ch


def print_open_tag(ch):
    global open_tag
    if open_tag == " ":
        return
    # dummy fix for bug < SHOULD BE REMOVED FOR FINAL RELEASE >
    open_tag.replace("<", "")
    if open_tag.strip() in SINGLE_TAGS:
        close_single_tag(open_tag.strip())
    else:
        print("Open TAG : < :", open_tag)
    open_tag = " "


def print_close_tag(ch):
    global close_tag
    if close_tag == " ":
        return
    print("Close TAG : </ :", close_tag)
    close_tag = " "


def add_doc_type(ch):
    global doc_type
    doc_type += ch


def print_doc_type(ch):
    global doc_type
    if doc_type == " ":
        return
    print("DOCTYPE :: ", doc_type[8:])
    doc_type = " "


def add_comment(ch):
    global comment
    comment += ch


def print_comment(ch):
    global comment
    if comment == " ":
        return
    print("COMMENT : ", comment)
    comment = " "


def adjust_comment(ch):
    global comment
    if comment[-1] == "-":
        comment = comment[:-1]


def add_attribute(ch):
    global attribute
    attribute += ch


def print_attribute(ch):
    global attribute
    if attribute == " ":
        return
    print("Attribute : ", attribute)
    attribute = " "


def add_attribute_value(ch):
    global attribute_value
    attribute_value += ch


def print_attribute_value(ch):
    global attribute_value
    if attribute_value == " ":
        return
    print("Attribute Value : ", attribute_value)
    attribute_value = " "


def add_tag_content(ch):
    global tag_content
    tag_content += ch


def print_tag_content(ch):
    global tag_content
    if tag_content == " ":
        return
    print("Tag content : ", open_tag, ":", tag_content)
    tag_content = " "


# Dummy data
autoM.add_transition("T_0", "T_0", "^[^<]$", add_tag_content)
# Tag opended
autoM.add_transition("T_0", "T_1", "^[<]$", print_tag_content)

# Tag recorder
autoM.add_transition("T_1", "T_1", "^[^\s>/!]$", add_open_tag)
# Attribute Processing
autoM.add_transition("T_1", "T_2", "^[\s]$", print_open_tag)
# Single tag closing
autoM.add_transition("T_1", "T_5", "^[>]$", print_open_tag)
# Close tag Processing
autoM.add_transition("T_1", "T_11", "^[/]$")
# Comment Processing start or doc type
autoM.add_transition("T_1", "T_6", "^[!]$")

# Attribute recorder
autoM.add_transition("T_2", "T_2", "^[^=>]$", add_attribute)
# tag closed "Unexpected"
autoM.add_transition("T_2", "T_5", "^[>]$")
# Attribute end
autoM.add_transition("T_2", "T_3", "^[=]$", print_attribute )

# Attribute value start
autoM.add_transition("T_3", "T_4", "^[\"]$")

# Attribute value recorder
autoM.add_transition("T_4", "T_4", "^[^\"]$", add_attribute_value)
# Attribute value end
autoM.add_transition("T_4", "T_1", "^[\"]$", print_attribute_value)

# Remove space in between tags
autoM.add_transition("T_5", "T_5", "^[\s]$")
# Unexpected text between tags
autoM.add_transition("T_5", "T_0", "^[^<\s]$", add_tag_content)
# New tag started
autoM.add_transition("T_5", "T_1", "^[<]$")

# Doc type Recorder
autoM.add_transition("T_6", "T_6", "^[^->]$", add_doc_type)
# Doc type end
autoM.add_transition("T_6", "T_5", "^[>]$", print_doc_type)
# if Comment start
autoM.add_transition("T_6", "T_7", "^[-]$")

# Confirm comment
autoM.add_transition("T_7", "T_8", "^[-]$")

# Comment Recorder
autoM.add_transition("T_8", "T_8", "^[^-]$", add_comment)
# Comment canel check
autoM.add_transition("T_8", "T_9", "^[-]$", add_comment)

# Comment Recorder continue
autoM.add_transition("T_9", "T_8", "^[^-]$", add_comment)
# Comment cancel confirmed
autoM.add_transition("T_9", "T_10", "^[-]$", adjust_comment)

# Comment canel complete
autoM.add_transition("T_10", "T_5", "^[>]$", print_comment)

# Close tag recorder
autoM.add_transition("T_11", "T_11", "^[^>]$", add_close_tag)
# Close tag closed
autoM.add_transition("T_11", "T_5", "^[>]$", print_close_tag)

# set end point
autoM.set_endpoint("T_5")

print(autoM)

#autoM.run('nothing random <tag attribute="attribute_value" attribute_2="attribute_value_2">')

"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

autoM.run(data)
