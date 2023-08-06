from selenium import webdriver
from driver.Requirements.GetRequirements import get_gecko_driver
import os
import re
import requests
import logging
import urllib.request


class WebProcessor:
    def __init__(self, show_window=False, req_user_input=False, logging_level=logging.INFO):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging_level)
        self.main_driver = None
        self.show_window = show_window
        if not get_gecko_driver(req_user_input):
            logging.error("failed getting gecko driver")

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
            logging.error(e)

    def stop(self):
        try:
            self.main_driver.close()
            self.main_driver.quit()
        except Exception as e:
            logging.error(e)

    def load_page(self, url):
        try:
            logging.info("loading driver...")
            self.main_driver.get(url)
            logging.info("finished loading driver")
        except Exception as e:
            logging.error(e)

    def download_img(self, file_name, direct=False, url=""):
        if direct:
            try:
                if url != "":
                    img_data = requests.get(url).content
                else:
                    img_data = requests.get(self.main_driver.current_url).content
                with open(file_name, 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                logging.error(e)
                return False, ""
            return True, file_name
        try:
            self.main_driver.save_screenshot(file_name)
        except Exception as e:
            logging.error(e)
            return False, ""
        return True, file_name

    def download_video(self, file_name, url=""):
        try:
            if len(url) == "":
                url = self.main_driver.current_url
            urllib.request.urlretrieve(url, file_name)
        except Exception as e:
            logging.error(e)
