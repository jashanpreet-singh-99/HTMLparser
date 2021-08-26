import os
from parser import Parser


"""Read the example file."""
EXAMPLE_FILE_1 = os.path.join(os.getcwd(), "html_example", "example_1.html")
example = open(EXAMPLE_FILE_1, 'r')
data = example.read()

html = Parser(data)
html.save_parsed_html("output/parsed_html_1.csv")

"""Read the example file."""
EXAMPLE_FILE_2 = os.path.join(os.getcwd(), "html_example", "example_2.html")
example = open(EXAMPLE_FILE_2, 'r')
data = example.read()

html_2 = Parser(data)
html_2.save_parsed_html("output/parsed_html_2.csv")
