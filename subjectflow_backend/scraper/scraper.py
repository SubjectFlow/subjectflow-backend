from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from subjectflow_backend.scraper.utils import ctrlClick, closeTab, switchTab
from selenium.webdriver.common.action_chains import ActionChains
import time

chrome_options = Options()
# chrome_options.headless = True
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


def scrape():
    driver.get("https://handbook.unimelb.edu.au/search/subjects")

    for element in driver.find_elements(By.CLASS_NAME, "search-result-item__anchor"):
        handleSubject(element=element)
    driver.quit()


def handleSubject(element: WebElement):
    originalTabHandle = driver.current_window_handle
    driver.execute_script("arguments[0].scrollIntoView();", element)
    ctrlClick(driver=driver, element=element)
    switchTab(driver=driver, windowIdx=1)
    time.sleep(2)
    closeTab(driver=driver)
    driver.switch_to.window(originalTabHandle)
