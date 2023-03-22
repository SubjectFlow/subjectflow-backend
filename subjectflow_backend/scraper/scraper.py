from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from subjectflow_backend.scraper.utils import ctrlClick, closeTab, switchTab, openTab
from selenium.webdriver.common.action_chains import ActionChains
import time

HANDBOOK = "https://handbook.unimelb.edu.au/"
YEAR = "2023"
chrome_options = Options()
# chrome_options.headless = True
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


def scrape():
    driver.get(HANDBOOK + "search/subjects")

    for element in driver.find_elements(By.CLASS_NAME, "search-result-item__code"):
        handleSubject(code=element.text)
    driver.quit()


def handleSubject(code: str):
    originalTabHandle = driver.current_window_handle
    openTab(
        driver=driver,
        url=HANDBOOK
        + "/"
        + YEAR
        + "/subjects/"
        + code
        + "/eligibility-and-requirements",
        name=code,
    )
    time.sleep(2)
    closeTab(driver=driver)
    driver.switch_to.window(originalTabHandle)
