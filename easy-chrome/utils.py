import functools
from contextlib import suppress

from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC


def ignore_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with suppress(Exception):
            return func(*args, **kwargs)

    return wrapper


class WaitList:
    ELE_SELECTOR = {'presence': EC.presence_of_element_located,
                    'visible': EC.visibility_of_element_located,
                    'invisible': EC.invisibility_of_element_located,
                    'clickable': EC.element_to_be_clickable}

    URL_SELECTOR = {
        'url_to_be': EC.url_to_be,
        'url_contains': EC.url_contains,
        'url_matches': EC.url_matches,
        'url_changes': EC.url_changes,
    }

    @classmethod
    def validate_value(cls, value):
        if isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return value
        else:
            raise TypeError(f"Invalid type for wait_list: {type(value)}, expected str or list")

    @classmethod
    def generate_wait_list(cls, user_wait_list, **kwargs) -> list:
        """
        generate wait-list from user_wait_list and kwargs
        :param user_wait_list: pre-defined ExpectedCondition
        :param kwargs: key-value pair for generate selenium expected condition
        :return: list of ExpectedCondition
        """
        wait_list = user_wait_list or []

        for key, value in kwargs.items():
            value = cls.validate_value(value)
            if key in cls.ELE_SELECTOR:
                for v in value:
                    wait_list.append(cls.ELE_SELECTOR[key]((By.XPATH, v)))
            elif key in cls.URL_SELECTOR:
                for v in value:
                    wait_list.append(cls.URL_SELECTOR[key](v))
            else:
                raise ValueError(f"Invalid key for wait_list: {key}, "
                                 f"expected: {list(cls.ELE_SELECTOR.keys()) + list(cls.URL_SELECTOR.keys())}")
        return wait_list
