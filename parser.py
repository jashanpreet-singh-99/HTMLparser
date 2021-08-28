import re
import os
import ast
import pandas as pd
import numpy as np
from automata import Automata

class HTMLElement:

    def __init__(self, row):
        self.tag = row['path'].split('|')[-2].strip()
        self.attributes = ast.literal_eval(row['attributes'])
        self.content = row['tag_content']

    def __str__(self):
        return "<" + self.tag + " " + str(self.attributes)[1:-1] + ">" + str(self.content) + "</" + self.tag + ">"

class Parser:

    __SINGLE_TAGS = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
                      'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']

    __COLUMNS = ["path", "attributes", "tag_content"]

    def __init__(self, data=None):
        self.__open_tag = ""
        self.__close_tag = ""
        self.__doc_type = ""
        self.__comment = ""
        self.__attribute = ""
        self.__attribute_value = ""

        self.__attribute_list = []
        self.__attribute_value_list = []

        self.__tag_content = ""

        self.__cur_tag_path = ""
        self.__parsed_html_db = pd.DataFrame(columns=self.__COLUMNS)

        self.__autoM = Automata()
        self.__init_parser_automata()
        if data != None:
            self.__autoM = self.parse(data)

    def __add_open_tag(self, ch):
        self.__open_tag += ch


    def __close_single_tag(self, ch):
        print("Closing Single_tag :", ch)
        self.__cur_tag_path = "|".join(ch) + "|"


    def __add_single_tag(self,ch):
        self.__cur_tag_path += ch + "|"
        print("Added Single_tag :", ch, self.__cur_tag_path)

    def __add_close_tag(self, ch):
        self.__close_tag += ch


    def __print_open_tag(self, ch):
        if self.__open_tag == "":
            return
        # dummy fix for bug < SHOULD BE REMOVED FOR FINAL RELEASE >
        self.__open_tag.replace("<", "")
        if self.__open_tag.strip() in self.__SINGLE_TAGS:
            self.__add_single_tag(self.__open_tag.strip())
        else:
            print("Open TAG : < :", self.__open_tag)
            self.__cur_tag_path += self.__open_tag + "|"
        self.__open_tag = ""

    def __print_open_tag_end(self, ch):
        if len(self.__attribute_list) > 0:
            print(self.__cur_tag_path, self.__attribute_list, self.__attribute_value_list)
        data_dict = {}
        data_dict[self.__COLUMNS[0]] = self.__cur_tag_path
        data_dict[self.__COLUMNS[1]] = str(dict(zip(self.__attribute_list, self.__attribute_value_list)))

        if self.__cur_tag_path.split("|")[-2].strip() in self.__SINGLE_TAGS:
            self.__close_single_tag(self.__cur_tag_path.split("|")[:-2])
        else:
            if self.__open_tag != "":
                self.__open_tag.replace("<", "")
                print("Open TAG : < :", self.__open_tag)
                self.__cur_tag_path += self.__open_tag + "|"
                data_dict[self.__COLUMNS[0]] = self.__cur_tag_path
                self.__open_tag = ""
        self.__parsed_html_db = self.__parsed_html_db.append(data_dict, ignore_index=True)
        self.__attribute_list = []
        self.__attribute_value_list = []

    def __print_close_tag(self, ch):
        if self.__close_tag == "":
            return
        print("Close TAG : </ :", self.__close_tag)
        if self.__cur_tag_path.split("|")[-2].strip() == self.__close_tag.strip():
            self.__cur_tag_path = "|".join(self.__cur_tag_path.split("|")[:-2]) + "|"
        self.__close_tag = ""

    def __add_doc_type(self, ch):
        self.__doc_type += ch

    def __print_doc_type(self, ch):
        if self.__doc_type == "":
            return
        print("DOCTYPE :: ", self.__doc_type[8:])
        self.__doc_type = ""

    def __add_comment(self, ch):
        self.__comment += ch

    def __print_comment(self, ch):
        if self.__comment == "":
            return
        print("COMMENT : ", self.__comment)
        self.__comment = ""

    def __adjust_comment(self, ch):
        if self.__comment[-1] == "-":
            self.__comment = self.__comment[:-1]

    def __add_attribute(self, ch):
        self.__attribute += ch

    def __print_attribute(self, ch):
        if self.__attribute == "":
            return
        print("Attribute : ", self.__attribute)
        self.__attribute_list.append(self.__attribute)
        self.__attribute = ""

    def __add_attribute_value(self, ch):
        self.__attribute_value += ch

    def __print_attribute_value(self, ch):
        if self.__attribute_value == "":
            return
        print("Attribute Value : ", self.__attribute_value)
        self.__attribute_value_list.append(self.__attribute_value)
        self.__attribute_value = ""

    def __add_tag_content(self, ch):
        self.__tag_content += ch

    def __print_tag_content(self, ch):
        if self.__tag_content == "":
            return
        print("Tag content : ", self.__open_tag, ":", self.__tag_content)
        index = len(self.__parsed_html_db) - 1
        if str(self.__parsed_html_db.at[index, self.__COLUMNS[-1]]) == 'nan':
            self.__parsed_html_db.at[index, self.__COLUMNS[-1]] = self.__tag_content
        else:
            self.__parsed_html_db.at[index, self.__COLUMNS[-1]] += self.__tag_content
        self.__tag_content = ""

    def __init_parser_automata(self):
        # Dummy data
        self.__autoM.add_transition("T_0", "T_0", "^[^<]$", self.__add_tag_content)
        # Tag opended
        self.__autoM.add_transition("T_0", "T_1", "^[<]$", self.__print_tag_content)

        # Tag recorder
        self.__autoM.add_transition("T_1", "T_1", "^[^\s>/!]$", self.__add_open_tag)
        # Attribute Processing
        self.__autoM.add_transition("T_1", "T_2", "^[\s]$", self.__print_open_tag)
        # Single tag closing
        self.__autoM.add_transition("T_1", "T_5", "^[>]$", self.__print_open_tag_end)
        # Close tag Processing
        self.__autoM.add_transition("T_1", "T_11", "^[/]$")
        # Comment Processing start or doc type
        self.__autoM.add_transition("T_1", "T_6", "^[!]$")

        # Attribute recorder
        self.__autoM.add_transition("T_2", "T_2", "^[^=>]$", self.__add_attribute)
        # tag closed "Unexpected"
        self.__autoM.add_transition("T_2", "T_5", "^[>]$", self.__print_open_tag_end)
        # Attribute end
        self.__autoM.add_transition("T_2", "T_3", "^[=]$", self.__print_attribute )

        # Attribute value start
        self.__autoM.add_transition("T_3", "T_4", "^[\"]$")

        # Attribute value recorder
        self.__autoM.add_transition("T_4", "T_4", "^[^\"]$", self.__add_attribute_value)
        # Attribute value end
        self.__autoM.add_transition("T_4", "T_1", "^[\"]$", self.__print_attribute_value)

        # Remove space in between tags
        self.__autoM.add_transition("T_5", "T_5", "^[\s]$")
        # Unexpected text between tags
        self.__autoM.add_transition("T_5", "T_0", "^[^<\s]$", self.__add_tag_content)
        # New tag started
        self.__autoM.add_transition("T_5", "T_1", "^[<]$")

        # Doc type Recorder
        self.__autoM.add_transition("T_6", "T_6", "^[^->]$", self.__add_doc_type)
        # Doc type end
        self.__autoM.add_transition("T_6", "T_5", "^[>]$", self.__print_doc_type)
        # if Comment start
        self.__autoM.add_transition("T_6", "T_7", "^[-]$")

        # Confirm comment
        self.__autoM.add_transition("T_7", "T_8", "^[-]$")

        # Comment Recorder
        self.__autoM.add_transition("T_8", "T_8", "^[^-]$", self.__add_comment)
        # Comment canel check
        self.__autoM.add_transition("T_8", "T_9", "^[-]$", self.__add_comment)

        # Comment Recorder continue
        self.__autoM.add_transition("T_9", "T_8", "^[^-]$", self.__add_comment)
        # Comment cancel confirmed
        self.__autoM.add_transition("T_9", "T_10", "^[-]$", self.__adjust_comment)

        # Comment canel complete
        self.__autoM.add_transition("T_10", "T_5", "^[>]$", self.__print_comment)

        # Close tag recorder
        self.__autoM.add_transition("T_11", "T_11", "^[^>]$", self.__add_close_tag)
        # Close tag closed
        self.__autoM.add_transition("T_11", "T_5", "^[>]$", self.__print_close_tag)

        # set end point
        self.__autoM.set_endpoint("T_5")

        print(self.__autoM)

    def parse(self, data):
        self.__autoM.run(data)
        print(self.__parsed_html_db)
        return self

    def save_parsed_html(self, file_name):
        self.__parsed_html_db.to_csv(file_name)

    def get_element_by_id(self, element):
        return self.get_element_by_attribute("id", element)

    def get_element_by_class(self, element):
        return self.get_element_by_attribute("class", element)
        # def check_attribute(attribute):
        #     a_dict = ast.literal_eval(attribute)
        #     if "class" in a_dict.keys():
        #         classes_list = a_dict['class'].split(" ")
        #         if element in classes_list:
        #             return True
        #     return False
        # if len(self.__parsed_html_db) < 1:
        #     print("Html data not parsed. Object empty.")
        #     return None
        # roi_db = self.__parsed_html_db[self.__parsed_html_db[self.__COLUMNS[1]].apply(check_attribute)]
        # element_list = []
        # for _,row in roi_db.iterrows():
        #     element_list.append(HTMLElement(row))
        # return element_list

    def get_element_by_attribute(self, attri, element):
        def check_attribute(attribute):
            a_dict = ast.literal_eval(attribute)
            if attri in a_dict.keys():
                value_list = a_dict[attri].split(" ")
                if element in value_list:
                    return True
            return False
        if len(self.__parsed_html_db) < 1:
            print("Html data not parsed. Object empty.")
            return None
        roi_db = self.__parsed_html_db[self.__parsed_html_db[self.__COLUMNS[1]].apply(check_attribute)]
        element_list = []
        for _,row in roi_db.iterrows():
            element_list.append(HTMLElement(row))
        return element_list
