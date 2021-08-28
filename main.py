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

element = html_2.get_element_by_id("site_name")
print(element[0])

element = html_2.get_element_by_attribute("id", "site_name")
print(element[0])

element_list = html_2.get_element_by_class("active")
[print(x) for x in element_list]

element_list = html_2.get_element_by_all_links()
[print(x.get_link()) for x in element_list]
