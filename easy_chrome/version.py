import os

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import DEFAULT_USER_HOME_CACHE_PATH
import shutil
import subprocess

from .utils import ignore_error


def get_driver_path():

    manager = ChromeDriverManager()
    os_type = manager.get_os_type()
    full_version = manager.driver.get_browser_version_from_os()

    if full_version is None and os_type == "win":
        full_version = _custom_get_win_chrome_version()

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


def _get_chrome_installed(hive, flag):
    """get installed chrome version from winreg"""
    try:
        import winreg

        a_reg = winreg.ConnectRegistry(None, hive)
        a_key = winreg.OpenKey(a_reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | flag)
        a_sub = winreg.OpenKey(a_key, "Google Chrome")
        return winreg.QueryValueEx(a_sub, "DisplayVersion")[0]
    except:
        pass


@ignore_error
def _custom_get_win_chrome_version():
    """get chromedriver version, download if needed"""
    import winreg
    try:
        if os.path.exists("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"):
            output = subprocess.check_output(
                r'wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" '
                r'get Version /value', shell=True)
        else:
            output = subprocess.check_output(
                r'wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" '
                r'get Version /value', shell=True)

        version = output.decode('utf-8').strip().split("=")[1]

        return version

    except:
        for hive, flag in ((winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY),
                           (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY),
                           (winreg.HKEY_CURRENT_USER, 0)):
            cr_ver = _get_chrome_installed(hive, flag)
            if cr_ver is not None:
                return cr_ver
