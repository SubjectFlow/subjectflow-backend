from functools import total_ordering
from enum import Enum
from subjectflow_backend.utils.dllist import DLList
from subjectflow_backend.scraper.logic import Expr, LogicOp, Literal, toDNF
from subjectflow_backend.scraper.scrapingConstants import HANDBOOK, YEAR
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import queue


@total_ordering
class OpPrecedence(Enum):
    OR = 0
    AND = 1
    OPTION = 2

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def getPrereqs(driver: webdriver, code: str):
    print("in " + code)
    driver.get(HANDBOOK + f"{YEAR}/subjects/{code}/eligibility-and-requirements")
    prereqs = driver.find_element(By.ID, "prerequisites")
    createPrereqLogic(elements=prereqs.find_elements(By.XPATH, "*"))
    return 1


def createPrereqLogic(elements: list[WebElement]):
    # print("creating")
    pq = queue.PriorityQueue()
    dll = DLList()
    allFlag = [True]
    # print(len(elements))
    try:
        for i in range(len(elements)):
            # print(i)
            if elements[i].tag_name == "table":
                # print(allFlag[0])
                dll.append(generateTableExpr(elements[i], allFlag))
                # print("post table")
            else:
                res = processText(elements[i].text, allFlag)
                # print("post process")
                if res[1] is not None:
                    # print("pre append")
                    node = dll.append(res[1])
                    # print("post append")
                    if isinstance(res[1], Expr):
                        # print("pre pq")
                        pq.put((res[0], i, node))
                        # print("post pq")
                # print("after pq if")

        # print("post parsing")

        # print("dll size: " + str(dll.size))
        if dll.size != 0:
            while not pq.empty():
                curr = pq.get()[2]
                # print("processing: " + str(curr.data.operator))
                curr.data.operands = (curr.prev.data, curr.next.data)
                # print(curr.data.operands)
                dll.remove(curr.prev)
                dll.remove(curr.next)

            # print('post loop dll size: ' +  str(dll.size))
            print(toDNF(dll.head.data))
    except Exception as e:
        print(e)


def processText(text: str, all: list[bool]):
    # print("processing text")
    text = text.lower().strip()
    # print(text)

    if "any of" in text or "one of" in text:
        # print('setting false')
        all[0] = False
        # print("any case")
        return (None, None)
    elif "both of" in text or "all of" in text:
        all[0] = True
        # print("all case")
        return (None, None)
    elif text == "and":
        # print("and case")
        return (OpPrecedence.AND, Expr(operator=LogicOp.AND, operands=(None, None)))
    elif text == "or":
        # print("or case")
        return (OpPrecedence.OR, Expr(operator=LogicOp.OR, operands=(None, None)))
    elif any(x in text for x in ("admission", "point", "provide")):
        # print("literal case")
        return (None, Literal(code=False, content=text))
    elif "option" in text and "option 1" not in text and "options" not in text:
        # print("option case")
        return (OpPrecedence.OPTION, Expr(operator=LogicOp.OR, operands=(None, None)))

    # print("returning (none, none)")
    return (None, None)


def generateTableExpr(table: WebElement, all: list[bool]):
    # print("generating")
    if all[0]:
        op = LogicOp.AND
    else:
        op = LogicOp.OR

    # print(table.text)

    codes = table.find_elements(By.XPATH, './/td[@data-label="Code"]')
    currExpr = Expr(operator=op, operands=(None, None))
    if len(codes) > 1:
        # print('> 1 rows case')
        currExpr.operands = (
            Literal(code=True, content=codes[0].text),
            Literal(code=True, content=codes[1].text),
        )
    elif len(codes) == 1:
        # print('1 row case')
        return Literal(code=True, content=codes[0].text)
    else:
        # print('0 rows case')
        return None

    # print(len(codes))
    for i in range(2, len(codes)):
        currExpr = Expr(
            operator=op, operands=(currExpr, Literal(code=True, content=codes[i].text))
        )

    all[0] = True
    return currExpr
