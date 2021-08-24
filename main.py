import re
import os
from automata import Automata

autoM = Automata()

open_tag = " "
close_tag = " "

def add_open_tag(ch):
    global open_tag
    open_tag += ch


def add_close_tag(ch):
    global close_tag
    close_tag += ch


def print_open_tag(ch):
    global open_tag
    if open_tag == " ":
        return
    print("Last open TAG value : < :", open_tag)
    open_tag = " "


def print_close_tag(ch):
    global close_tag
    if close_tag == " ":
        return
    print("Last close TAG : </ :", close_tag)
    close_tag = " "


# Dummy data
autoM.add_transition("T_0", "T_0", "^[^<]$")
# Tag opended
autoM.add_transition("T_0", "T_1", "^[<]$")

# Tag recorder
autoM.add_transition("T_1", "T_1", "^[^\s>/]$", add_open_tag)
# Attribute Processing
autoM.add_transition("T_1", "T_2", "^[\s]$", print_open_tag)
# Single tag closing
autoM.add_transition("T_1", "T_5", "^[>]$", print_open_tag)
# Close tag Processing
autoM.add_transition("T_1", "T_11", "^[/]$")

# Attribute Value
autoM.add_transition("T_2", "T_2", "^[^=>]$")
# tag closed "Unexpected"
autoM.add_transition("T_2", "T_5", "^[>]$")
# Attribute recorder
autoM.add_transition("T_2", "T_3", "^[=]$")

# Attribute value start
autoM.add_transition("T_3", "T_4", "^[\"]$")

# Attribute value recorder
autoM.add_transition("T_4", "T_4", "^[^\"]$")
# Attribute value end
autoM.add_transition("T_4", "T_1", "^[\"]$")

# Remove space in between tags
autoM.add_transition("T_5", "T_5", "^[\s]$")
# Unexpected text between tags
autoM.add_transition("T_5", "T_0", "^[^<\s]$")
# New tag started
autoM.add_transition("T_5", "T_1", "^[<]$")

# Close tag recorder
autoM.add_transition("T_11", "T_11", "^[^>]$", add_close_tag)
# Close tag closed
autoM.add_transition("T_11", "T_5", "^[>]$", print_close_tag)

# set end point
autoM.set_endpoint("T_5")

print(autoM)

#autoM.run('nothing random <tag attribute="attribute_value" attribute_2="attribute_value_2">')

"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_1.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

autoM.run(data)
