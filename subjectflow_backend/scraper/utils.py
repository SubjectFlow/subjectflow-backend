from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def ctrlClick(driver: webdriver, element: WebElement):
    ActionChains(driver).key_down(Keys.CONTROL).click(element).key_up(
        Keys.CONTROL
    ).perform()


def closeTab(driver: webdriver):
    driver.close()


def switchTab(driver: webdriver, windowIdx: int):
    driver.switch_to.window(driver.window_handles[windowIdx])


def openTab(driver: webdriver, url: str, name: str):
    driver.execute_script("window.open('" + url + "', '" + name + "')")
    driver.switch_to.window(name)
