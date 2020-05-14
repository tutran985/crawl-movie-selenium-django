from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import logging


class CommonAction:
    def __init__(self, driver):
        self.driver = driver

    def get_link(self, url):
        self.driver.get(url)

    def set_value(self, xpath, value):
        input = self.driver.find_element_by_xpath(xpath)

        self.driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', input, value)

    def get_xpath_from_index(self, container_path, sub_element_path, index):
        return container_path + "[%d]" % index + sub_element_path

    def scroll_to_element(self, control):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', control)

    def scroll_into_view(self, xpath):
        control = self.driver.find_element_by_xpath(xpath)
        self.scroll_to_element(control)

    def click(self, xpath):
        control = self.driver.find_element_by_xpath(xpath)
        self.scroll_to_element(control)
        control.click()

    def click_by_execute_script(self, xpath):
        executed_script = "document.evaluate(\"%s\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()" % xpath
        # click on use a new card
        self.driver.execute_script(executed_script)

    def send_key(self, xpath, value=""):
        control = self.driver.find_element_by_xpath(xpath)
        self.scroll_to_element(control)
        control.send_keys(value)

    def wait_until_element_clickable(self, xid, wait_seconds=40):
        wait = WebDriverWait(self.driver, wait_seconds)
        wait.until(ec.element_to_be_clickable((By.ID, xid)))

    def wait_until_element_visible(self, xpath, wait_seconds=40):
        wait = WebDriverWait(self.driver, wait_seconds)
        wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))


    def wait_until_element_invisible(self, xpath, wait_seconds=40):
        wait = WebDriverWait(self.driver, wait_seconds)
        wait.until(ec.invisibility_of_element_located((By.XPATH, xpath)))


    def get_text(self, xpath):
        control = self.driver.find_element_by_xpath(xpath)
        return control.text

    def get_attribute(self, xpath, attribute):
        control = self.driver.find_element_by_xpath(xpath)
        return control.get_attribute(attribute)

    def get_number_of_elements(self, xpath):
        element_list = self.driver.find_elements_by_xpath(xpath)
        return len(element_list)

    def select_dropdown_menu_item(self, xpath, value):
        element_option = self.driver.find_element_by_xpath(
            xpath + "//option[@value='%s']" % value)

        element_option.click()

    def select_dropdown_menu_item_by_text(self, xpath, text):
        element_option = self.driver.find_element_by_xpath(
            xpath + "//option[text()='%s']" % text)

        element_option.click()

    def get_text_from_elements(self, xpath):
        elements = self.driver.find_elements_by_xpath(xpath)
        result = []
        for element in elements:
            result.append(element.text)
        return result

    def switch_to_frame(self, xpath):
        iframe = self.driver.find_element_by_xpath(xpath)
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
