from __future__ import annotations
from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from .utils import ignore_error, WaitList
from .element import Element
from .version import driver_path


class Driver(webdriver.Chrome):
    _default_wait_time = 30

    @classmethod
    def set_chrome(cls,
                   detach_mode: bool = False,
                   headless: bool = False,
                   download_dir: str = None,
                   proxy="",
                   other_args: list = None,
                   other_options: dict = None):
        """
        :param detach_mode: chrome detach mode, default False
        :param headless: run in headless mode or not, default False
        :param download_dir: download directory
        :param proxy: proxy_server:port
        :param other_args: other arguments to add to chrome options
        :param other_options: other experimental options to add to chrome options
        :return: Chrome WebDriver
        """
        chrome_options = webdriver.ChromeOptions()

        if headless:
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless=new")

        # add default experimental options
        chrome_options.add_experimental_option("excludeSwitches",
                                               ["ignore-certificate-errors",
                                                "safebrowsing-disable-download-protection",
                                                "safebrowsing-disable-auto-update",
                                                "disable-client-side-phishing-detection",
                                                'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("detach", detach_mode)

        # add default argument
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")

        # add download directory
        if download_dir is not None:
            prefs = {"download.default_directory": os.path.abspath(download_dir)}
            chrome_options.add_experimental_option("prefs", prefs)

        # add proxy server
        if ":" in str(proxy):
            chrome_options.add_argument('--proxy-server=http://{}'.format(proxy))

        # add user arguments
        if other_args:
            for arg in other_args:
                chrome_options.add_argument(arg)

        # add user experimental options
        if other_options:
            for k, v in other_options.items():
                chrome_options.add_experimental_option(name=k, value=v)

        return cls(service=Service(driver_path.path), options=chrome_options)

    def _wait(self, wait_time=_default_wait_time):
        return WebDriverWait(self, wait_time)

    def wait_presence(self, xpath: str, wait_time: int = _default_wait_time, message: str | None = None) -> Element:
        """
        shortcut to wait for element to presence in DOM
        :param xpath: xpath of element
        :param wait_time: wait time
        :param message: message for exception
        :return: element as custom Element
        """

        return Element(self._wait(wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)),
                                                   message=message or f"wait_presence, xpath: {xpath}"))

    def wait_visible(self, xpath: str, wait_time: int = _default_wait_time, message: str | None = None) -> Element:
        """wait element to be visible
        :param xpath: xpath of element
        :param wait_time: wait time
        :param message: message for exception
        :return: element as custom Element
        """
        return Element(self._wait(wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)),
                                                   message=message or f"wait_visible, xpath: {xpath}"))

    def wait_invisible(self, xpath: str, wait_time: int = _default_wait_time, message: str | None = None) -> Element:
        """
        wait element to be invisible
        :param xpath: xpath of element
        :param wait_time: wait time
        :param message: message for exception
        :return: element as custom Element
        """

        return Element(self._wait(wait_time).until(EC.invisibility_of_element_located((By.XPATH, xpath)),
                                                   message=message or f"wait_invisible, xpath: {xpath}"))

    def wait_clickable(self, xpath: str, wait_time: int = _default_wait_time, message: str | None = None) -> Element:
        """wait element to be clickable
        :param xpath: xpath of element
        :param wait_time: wait time
        :param message: message for exception
        :return: element as custom Element
        """
        return Element(self._wait(wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)),
                                                   message=message or f"wait_clickable, xpath: {xpath}"))

    def wait_any_of(self,
                    user_wait_list: list | None = None,
                    timeout_message: str = "",
                    wait_time: int = _default_wait_time,
                    wait_info: dict[str, str | list] = None):
        """
        wait all conditions to be true
        :param user_wait_list: predefined ExpectedCondition list
        :param timeout_message: message to show when timeout
        :param wait_time: wait time
        :param wait_info: key, pair values to generate ExpectedCondition,
            - url_to_be, url_contains, url_matches, url_changes,
            - presence, visible, invisible, clickable
        :return: True if ok, else raise TimeOutError with timeout_message
        """
        wait_info = wait_info or {}
        wait_list = WaitList.generate_wait_list(user_wait_list, **wait_info)
        self._wait(wait_time).until(EC.any_of(*wait_list), message=timeout_message)

    def wait_all_of(self,
                    user_wait_list: list | None = None,
                    timeout_message: str = "",
                    wait_time: int = _default_wait_time,
                    wait_info: dict[str, str | list] = None):
        """
        wait all conditions to be true
        :param user_wait_list: predefined ExpectedCondition list
        :param timeout_message: message to show when timeout
        :param wait_time: wait time
        :param wait_info: dict of key, pair values to generate ExpectedCondition, key in
            - url_to_be, url_contains, url_matches, url_changes,
            - presence, visible, invisible, clickable
        :return: True if ok, else raise TimeOutError with timeout_message
        """
        wait_info = wait_info or {}
        wait_list = WaitList.generate_wait_list(user_wait_list, **wait_info)
        return self._wait(wait_time).until(EC.all_of(*wait_list), message=timeout_message)

    def wait_none_of(self,
                     user_wait_list: list | None = None,
                     timeout_message: str = "",
                     wait_time: int = _default_wait_time,
                     wait_info: dict[str, str | list] = None):
        """
        wait none of the conditions to be true
        :param user_wait_list: predefined ExpectedCondition list
        :param timeout_message: message to show when timeout
        :param wait_time: wait time
        :param wait_info: key, pair values to generate ExpectedCondition,
            - url_to_be, url_contains, url_matches, url_changes,
            - presence, visible, invisible, clickable
        :return: True if ok, else raise TimeOutError with timeout_message
        """
        wait_info = wait_info or {}
        wait_list = WaitList.generate_wait_list(user_wait_list, **wait_info)
        return self._wait(wait_time).until(EC.none_of(*wait_list), message=timeout_message)

    def get_element(self, xpath) -> Element:
        """shortcut for get element by Xpath"""
        return Element(self.find_element(by=By.XPATH, value=xpath))

    def get_elements(self, xpath) -> list[Element]:
        """shortcut for get list of elements by Xpath"""
        return [Element(item) for item in self.find_elements(by=By.XPATH, value=xpath)]

    def find_element_by_xpath(self, xpath) -> Element:
        """method get element by Xpath"""
        return self.get_element(xpath)

    def find_elements_by_xpath(self, xpath) -> list[Element]:
        """get list of elements by Xpath"""
        return self.get_elements(xpath)

    def get_session_storage(self, key):
        """
        :param key: session storage key to get
        """
        return self.execute_script("return window.sessionStorage.getItem(arguments[0]);", key)

    def set_session_storage(self, key, value):
        """
        :param key: session storage key
        :param value: session storage value
        """
        self.execute_script("return window.sessionStorage.setItem(arguments[0], arguments[1]);", key, value)

    def get_local_storage_keys(self):
        """
        :return: get all current driver local storage keys
        """
        return self.execute_script("return Object.keys(window.localStorage);")

    def get_local_storage(self, key):
        """
        :param key: local storage key to get
        """
        return self.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set_local_storage(self, key, value):
        """
        :param key: local storage key
        :param value: local storage value
        """
        self.execute_script("return window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def remove_local_storage(self, key: str):
        """
        :param key: local storage key to remove
        """
        self.set_local_storage(key, "")
        self.execute_script("return window.localStorage.removeItem(arguments[0]);", key)

    def get_cookies_string(self):
        """
        :return: current driver cookies in key=value; key=value format
        """
        cookies = self.get_cookies()
        cookies_string = '; '.join(['{}={}'.format(cookie['name'], cookie['value']) for cookie in cookies])
        return cookies_string

    def get_user_agent(self):
        """
        :return: get current driver user agent
        """
        return self.execute_script("return navigator.userAgent;")

    def expand_shadow_element(self, element: WebElement):
        """
        :param element: element which has shadow root
        :return: tree under shadow root
        """
        return self.execute_script('return arguments[0].shadowRoot', element)

    @property
    def user_agent(self):
        """
        :return: user_agent as property
        """
        return self.execute_script("return navigator.userAgent;")

    @property
    def is_ready(self):
        return self.execute_script("return document.readyState") == "complete"

    def wait_redirected(self, limit_redirect=4, limit_time=20):
        """
        sometime page is continuously redirected, this function will wait for some completed redirection
        """
        for tr in range(limit_redirect):
            counter = 0
            while True:
                counter += 0.5
                sleep(0.5)
                if self.is_ready or counter > limit_time:
                    break

    @ignore_error
    def remove_element(self, element: Element | WebElement):
        """
        remove element from DOM, surround with try catch, so it will not raise error if element is not found
        """
        self.execute_script("var element = arguments[0];element.parentNode.removeChild(element);", element)

    @ignore_error
    def remove_element_by_xpath(self, xpath, delay_before: float = 0.5, delay_after: float = 0.5):
        """
        remove element from DOM by xpath
        """
        sleep(delay_before)
        ele = self.get_element(xpath)
        self.remove_element(ele)
        sleep(delay_after)
