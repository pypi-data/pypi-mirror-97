from selenium import webdriver
from driver.Requirements.GetRequirements import get_gecko_driver
import os
import re
import requests


class WebFilter:
    def __init__(self):
        self.data = {}
        self.filter_attribution = "_attribute"
        self.filter_class = "_class"
        self.filter_class = "_tag"
        self.filter_class = "_id"
        self.filter_class = "_text"
        self.filter_contains = "_contains"
        self.get_count = "count"
        self.get_text = "text"

    def get_filters(self):
        return self.data


class WebProcessor:
    def __init__(self, show_window=False,req_user_input=False):
        self.main_driver = None
        self.show_window = show_window
        if not get_gecko_driver(req_user_input):
            print("failed getting gecko driver")

    def load(self):
        try:
            if self.show_window:
                self.main_driver = webdriver.Firefox()
            else:
                os.environ['MOZ_HEADLESS'] = '1'
                os.environ['MOZ_HEADLESS_HEIGHT'] = '1080'
                os.environ['MOZ_HEADLESS_WIDTH'] = '1920'
                self.main_driver = webdriver.Firefox()
        except Exception as e:
            print(e)

    def stop(self):
        try:
            self.main_driver.close()
            self.main_driver.quit()
        except Exception as e:
            print("Failed to close driver",e)

    def load_page(self, url):
        try:
            self.main_driver.get(url)
        except Exception as e:
            print("load_page error:", e)

    def filter_elements(self, filters):
        current_data = self.main_driver
        for k in filters.keys():
            if k == "skip":
                continue
            if k == "count":
                return len(current_data)
            if isinstance(current_data,list):
                new_data = []
                for i in current_data:
                    passed, data = self.get_element(k, filters[k],
                                                    previous_elements=i)
                    if passed:
                        if len(data) > 0:
                            if isinstance(data,list):
                                new_data += data
                            else:
                                new_data.append(data)
                if len(new_data) == 1:
                    current_data = new_data[0]
                else:
                    current_data = new_data
                continue
            passed, data = self.get_element(k, filters[k],
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
            previous_elements = self.main_driver
        if re.search("_tag", element_type):
            try:
                output = previous_elements.find_elements_by_tag_name(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output

        if re.search("_id", element_type):
            try:
                output = previous_elements.find_elements_by_id(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output

        if re.search("_class", element_type):
            try:
                output = previous_elements.find_elements_by_class_name(name)
            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search("_attribute", element_type):
            try:
                output = previous_elements.get_attribute(name)

            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search("_text", element_type):
            try:
                output = previous_elements.text
            except Exception as E:
                print(E)
                return False, None
            return True, output
        if re.search("_contains",element_type):
            if re.search(name,previous_elements):
                return True ,previous_elements
            return True, ""
        return False,""

    def download_img(self, file_name, direct=False,url=""):
        if direct:
            try:
                img_data = requests.get(url).content
                with open(file_name, 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                print(e)
                return False, ""
            return True, file_name
        try:
            self.main_driver.save_screenshot(file_name)
        except Exception as e:
            print(e)
            return False, ""
        return True, file_name
