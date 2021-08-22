import re
import os
from automata import Automata

autoM = Automata()

autoM.add_transition("T_0", "T_0", "^[^<]$")
autoM.add_transition("T_0", "T_1", "^[<]$")
autoM.add_transition("T_1", "T_1", "^[^\s>]$")
autoM.add_transition("T_1", "T_2", "^[\s]$")
autoM.add_transition("T_1", "T_5", "^[>]$")
autoM.add_transition("T_2", "T_2", "^[^=>]$")
autoM.add_transition("T_2", "T_5", "^[>]$")
autoM.add_transition("T_2", "T_3", "^[=]$")
autoM.add_transition("T_3", "T_4", "^[\"]$")
autoM.add_transition("T_4", "T_4", "^[^\"]$")
autoM.add_transition("T_4", "T_1", "^[\"]$")
autoM.set_endpoint("T_5")
autoM.add_transition("T_5", "T_5", "^[\s]$")
autoM.add_transition("T_5", "T_0", "^[^<\s]$")
autoM.add_transition("T_5", "T_1", "^[<]$")

print(autoM)

autoM.run('nothing random <tag attribute="attribute_value" attribute_2="attribute_value_2">')

"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

autoM.run(data)
