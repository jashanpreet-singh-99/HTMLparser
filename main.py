import os
from parser import Parser


"""Read the example file."""
EXAMPLE_FILE = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE, 'r')
data = example.read()

html = Parser(data)
html.save_parsed_html("parsed_html.csv")
