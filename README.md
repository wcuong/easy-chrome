# Easy Chrome

## Description

This package is used as an extension to selenium chrome WebDriver. It contains shortcuts to control driver more easily.

## Features

1. Auto download chromedriver by webdriver_manager with custom cache.
2. Shortcuts to control driver and element.


## Examples

- init chrome driver.

```
from easy_chrome import Driver
driver = Driver.set_chrome(detach_mode=True)
```

- wait an element located by XPATH to be visible in DOM.

```
// bare usage
WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath))

// with easy-chrome
driver.wait_visible(xpath)
```

- get local storage.

```
// bare usage
driver.execute_script("return window.sessionStorage.getItem(arguments[0]);", key)

// with easy-chrome
driver.get_local_storage(key)
```

- wait username input field to be visible in DOM, clear the content and write username to it.

```
input_xpath = "//input[@id='username']

// bare usage
WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, input_xpath)).clear()
sleep(0.2)
WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, input_xpath)).sendkeys(username)

// with easy-chrome
driver.wait_visible(input_xpath).clear_and_type(user_name)
```

## Source Code

The source code is currently hosted on GitHub at: https://github.com/wcuong/easy-chrome


## Release

The package is currently hosted on Pypi at: https://pypi.org/project/easy-chrome/


## ChangeLog
### 2.0.1 2023-11-04
- Init project
    
### 2.0.2 2023-11-06
- Change headless mode to --headless=new
- Ignore DownloadBubble Feature, which enforces an download popup in incognito mode.

### 2.0.3 2023-11-08
- add custom windows chrome detect method because sometimes webdriver_manager fails to detect.
