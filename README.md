# Easy Chrome

## Description

This package is used as an extension to selenium chrome WebDriver. It contains shortcuts to control driver more easily.

## Features

1. Auto download chromedriver by webdriver_manager with custom cache.
2. Shortcuts to control driver and element.


## Samples

- init chrome driver.

```
from easy-chrome import Driver
driver = Driver.set_chrome(headless=True)
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
driver.get_local_storage()
```