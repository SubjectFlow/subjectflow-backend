from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from subjectflow_backend.scraper.utils import ctrlClick, closeTab, switchTab, openTab
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor, wait
from dotenv import dotenv_values
from pymongo import MongoClient
from subjectflow_backend.models.subject import Subject, UpdateSubject
import subjectflow_backend.api.subjectApi as subjectApi
import time
import asyncio

HANDBOOK = "https://handbook.unimelb.edu.au/"
YEAR = "2023"
config = dotenv_values(".env")
db = MongoClient(config["MONGO_CONNECTION_STRING"])[config["DB_NAME"]]

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument("log-level=2")
chrome_options.add_argument("--window-size=1920,1080")


def scrape():
    pages = getNumPages()
    # asyncio.run(postAllSubjects(pages=pages))
    asyncio.run(postAllPrereqs(pages=pages))


async def postAllSubjects(pages: int):
    await subjectApi.dropAllSubjects(db=db)
    futures = []
    with ThreadPoolExecutor() as executor:
        for i in range(1, pages + 1):
            futures.append(executor.submit(postSubjectsOnPage, i))

    wait(futures)


def postSubjectsOnPage(page: int):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(getHandbookPageUrl(page=page))
    subjects: list(Subject) = []
    for element in driver.find_elements(By.CLASS_NAME, "search-result-item__name"):
        subject: Subject = Subject(
            name=element.find_element(By.TAG_NAME, "h3").text,
            code=element.find_element(By.TAG_NAME, "span").text,
        )
        subjects.append(subject)

    asyncio.run(subjectApi.postSubjects(db, subjects))
    driver.quit()


async def postAllPrereqs(pages: int):
    futures = []
    with ThreadPoolExecutor() as executor:
        for i in range(1, pages + 1):
            futures.append(executor.submit(postPrereqsOnPage, i))

    wait(futures)


def postPrereqsOnPage(page: int):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(getHandbookPageUrl(page=page))
    updateInfo: list[tuple[str, list[UpdateSubject]]] = []
    for element in driver.find_elements(By.CLASS_NAME, "search-result-item__header"):
        try:
            element.find_element(By.CLASS_NAME, "search-result-item__flag--highlight")
            code: str = element.find_element(
                By.CLASS_NAME, "search-result-item__code"
            ).text
            updateInfo.append((code, getPrereqs(driver=driver, code=code)))
        except:
            pass

    driver.quit()


def getPrereqs(driver: webdriver, code: str):
    print("in " + code)
    driver.get(HANDBOOK + f"{YEAR}/subjects/{code}/eligibility-and-requirements")
    prereq = driver.find_element(By.ID, "prerequisites")
    print(prereq.find_elements(By.XPATH, "*"))


def getHandbookPageUrl(page: int) -> str:
    return (
        HANDBOOK
        + f"search?types%5B%5D=subject&year={YEAR}&subject_level_type%5B%5D=all&study_periods%5B%5D=all&area_of_study%5B%5D=all&org_unit%5B%5D=all&campus_and_attendance_mode%5B%5D=all&page={page}&sort=_score%7Cdesc"
    )


def getNumPages() -> int:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(HANDBOOK + "subjects")
    pages = 2
    # pages = int(
    #     driver.find_element(By.CLASS_NAME, "search-results__paginate")
    #     .find_element(By.TAG_NAME, "span")
    #     .text[3:]
    # )
    driver.quit()
    return pages
