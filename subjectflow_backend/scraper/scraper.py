from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from subjectflow_backend.scraper.utils import ctrlClick, closeTab, switchTab, openTab
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor, wait
import time

HANDBOOK = "https://handbook.unimelb.edu.au/"
YEAR = "2023"
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument("log-level=2")
chrome_options.add_argument("--window-size=1920,1080")


def scrape():
    print(__name__)
    postAllSubjects()
    # for element in driver.find_elements(By.CLASS_NAME, "search-result-item__code"):
    #     handleSubject(code=element.text)


def postAllSubjects():
    futures = []
    driver = webdriver.Chrome(options=chrome_options)
    pages = getNumPages(driver=driver)
    driver.quit()
    with ThreadPoolExecutor() as executor:
        for i in range(1, pages + 1):
            futures.append(executor.submit(postSubjectsOnPage, i))

    wait(futures)


def postSubjectsOnPage(page: int):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(getHandbookPageUrl(page=page))
    for element in driver.find_elements(By.CLASS_NAME, "search-result-item__name"):
        print(element.find_element(By.TAG_NAME, "h3").text)

    driver.quit()


# def handleSubject(code: str):
#     originalTabHandle = driver.current_window_handle
#     openTab(
#         driver=driver,
#         url=HANDBOOK
#         + "/"
#         + YEAR
#         + "/subjects/"
#         + code
#         + "/eligibility-and-requirements",
#         name=code,
#     )
#     time.sleep(2)
#     closeTab(driver=driver)
#     driver.switch_to.window(originalTabHandle)


def getHandbookPageUrl(page: int) -> str:
    return (
        HANDBOOK
        + f"search?types%5B%5D=subject&year={YEAR}&subject_level_type%5B%5D=all&study_periods%5B%5D=all&area_of_study%5B%5D=all&org_unit%5B%5D=all&campus_and_attendance_mode%5B%5D=all&page={page}&sort=_score%7Cdesc"
    )


def getNumPages(driver: webdriver) -> int:
    driver.get(HANDBOOK + "subjects")
    return int(
        driver.find_element(By.CLASS_NAME, "search-results__paginate")
        .find_element(By.TAG_NAME, "span")
        .text[3:]
    )
