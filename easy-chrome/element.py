"""
    This module is an extension for selenium WebElement, with some useful custom functions
    - clear and type: use to clear input field, then type content
        eg: self.clear_and_type('abc')
    - select methods: methods to direct implement select from web Element (not via Select class)
        eg: self.select_visible_text("option1")
    - get element(s): shortcuts for find_element by XPATH
    - wait and click: shortcuts for wait sometime before and after click
    - wait
"""

from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from time import sleep


class Element(WebElement):
    def __init__(self, element: WebElement):
        super().__init__(parent=element.parent, id_=element.id)

    def clear_and_type(self, content: str):
        """clear input and type content"""
        self.clear()
        sleep(0.5)
        self.send_keys(content)

    def select_value(self, value):
        """select element by value"""
        Select(self).select_by_value(value)

    def select_visible_text(self, text):
        """select element by text"""
        Select(self).select_by_visible_text(text)

    def select_index(self, index):
        """select element by index"""
        Select(self).select_by_index(index)

    def get_element(self, xpath) -> Element:
        """get element by Xpath from root element"""
        return Element(self.find_element(by=By.XPATH, value=xpath))

    def get_elements(self, xpath) -> list[Element]:
        """get list of elements by Xpath from root element"""
        return [Element(item) for item in self.find_elements(by=By.XPATH, value=xpath)]

    def find_element_by_xpath(self, xpath) -> Element:
        """get element by Xpath from root element"""
        return self.get_element(xpath)

    def find_elements_by_xpath(self, xpath) -> list[Element]:
        """get list of elements by Xpath from root element"""
        return self.get_elements(xpath)

    def wait_and_click(self, bef: float = 0.5, aft: float = 0):
        """
        wait sometime before and after click
        """
        sleep(bef)
        self.click()
        sleep(aft)

    def wait(self, wait_time: float = 0.5) -> Element:
        """
            builder pattern for wait
        """
        sleep(wait_time)
        return self
