import re
import json
from driver.WebProcessor.WebProcessor import WebProcessor
import logging

FILTER_ATTRIBUTE = "_attribute"
FILTER_CLASS = "_class"
FILTER_TAG = "_tag"
FILTER_ID = "_id"
FILTER_TEXT = "_text"
FILTER_CONTAINS = "_contains"
FILTER_COUNT = "_count"


class WebFilter:
    def __init__(self,web_processor):
        self.possible_values = [FILTER_ATTRIBUTE, FILTER_CLASS, FILTER_TAG, FILTER_ID, FILTER_TEXT, FILTER_CONTAINS,
                                FILTER_COUNT]
        self.data = {}
        self.web_processor = web_processor

    def get_filters(self):
        return self.data

    def load_filter(self, filename):
        try:
            settings_file = "".join(open(filename).readlines())
            self.data = json.loads(settings_file)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def save_filter(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.data, indent=4))

    def add_filter_data(self, filter_type, filter_data, filter_name=""):
        if filter_name == "":
            filter_name = str(len(self.data))
        if filter_type in self.possible_values:
            if filter_name + filter_type in self.data:
                logging.warning(
                    "overwriting " + filter_name + filter_type + " : " + self.data[filter_name + filter_type])
            self.data[filter_name + filter_type] = filter_data
            return True
        logging.error("invalid filter type, Possible Filter Values:" + str(self.possible_values))
        return False

    def clear(self):
        self.data = {}

    def filter_elements(self):
        current_data = self.web_processor.main_driver
        for k in self.data.keys():
            if k == "skip":
                continue
            if k == "count":
                return len(current_data)
            if isinstance(current_data, list):
                new_data = []
                for i in current_data:
                    passed, data = self.get_element(k, self.data[k],
                                                    previous_elements=i)
                    if passed:
                        if len(data) > 0:
                            if isinstance(data, list):
                                new_data += data
                            else:
                                new_data.append(data)
                if len(new_data) == 1:
                    current_data = new_data[0]
                else:
                    current_data = new_data
                continue
            passed, data = self.get_element(k, self.data[k],
                                            previous_elements=current_data)
            if passed:
                if len(data) > 0:
                    current_data = data
            else:
                print("invalid filter")
                return None
        return current_data

    def get_element(self, element_type, name, previous_elements=None):
        if previous_elements is None:
            previous_elements = self.web_processor.main_driver
        if re.search(FILTER_TAG, element_type):
            try:
                output = previous_elements.find_elements_by_tag_name(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output

        if re.search(FILTER_ID, element_type):
            try:
                output = previous_elements.find_elements_by_id(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output

        if re.search(FILTER_CLASS, element_type):
            try:
                output = previous_elements.find_elements_by_class_name(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search(FILTER_ATTRIBUTE, element_type):
            try:
                output = previous_elements.get_attribute(name)

            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search(FILTER_TEXT, element_type):
            try:
                output = previous_elements.text
            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search(FILTER_CONTAINS, element_type):
            if re.search(name, previous_elements):
                return True, previous_elements
            return True, ""
        return False, ""
