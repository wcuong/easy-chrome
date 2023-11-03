import os
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import DEFAULT_USER_HOME_CACHE_PATH
import shutil


def get_driver_path():

    manager = ChromeDriverManager()
    os_type = manager.get_os_type()
    full_version = manager.driver.get_browser_version_from_os()
    main_version = full_version.split(".")[0] if full_version else None
    # caching by main_version only
    if os_type == "win":
        file_name = f"chromedriver_{main_version}.exe"
    else:
        file_name = f"chromedriver_{main_version}"

    expect_path = os.path.join(DEFAULT_USER_HOME_CACHE_PATH, file_name)

    if not os.path.exists(expect_path):
        wdm_path = ChromeDriverManager(driver_version=full_version).install()
        shutil.copy(wdm_path, expect_path)

    return expect_path


class DriverPath:
    def __init__(self):
        self._path = None

    @property
    def path(self):
        if self._path is None:
            self._path = get_driver_path()
        return self._path


driver_path = DriverPath()
