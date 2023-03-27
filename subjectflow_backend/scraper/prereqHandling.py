from functools import total_ordering
from enum import Enum
from subjectflow_backend.utils.dllist import DLList
from subjectflow_backend.scraper.logic import Expr, LogicOp, Literal, toDNF
from subjectflow_backend.scraper.scrapingConstants import HANDBOOK, YEAR
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from dataclasses import dataclass
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


class prereqScrapingFlags:
    andTableMode: bool = True
    readingList: bool = False


@dataclass
class processTextRes:
    content: Expr | Literal
    firstInList: bool = False
    precedence: OpPrecedence | None = None


def getPrereqs(driver: webdriver, code: str):
    print("\nin " + code)
    driver.get(HANDBOOK + f"{YEAR}/subjects/{code}/eligibility-and-requirements")
    prereqs = driver.find_element(By.ID, "prerequisites")
    elements = prereqs.find_elements(By.XPATH, "*")
    # print("creating")
    pq = queue.PriorityQueue()
    dll = DLList()
    flags = prereqScrapingFlags()
    listCondition: Literal | None = None
    # print(len(elements))
    try:
        for i in range(len(elements)):
            # print(i)
            if elements[i].tag_name == "table":
                # print(flags[0])
                dll.append(generateTableExpr(elements[i], flags))
                # print("post table")
            else:
                res = processText(elements[i].text, flags)
                if flags.readingList and isinstance(res.content, Literal):
                    if res.firstInList:
                        listCondition = res.content
                    else:
                        listCondition.content += "\n" + res.content.content
                else:
                    if listCondition is not None:
                        dll.append(listCondition)
                        listCondition = None
                    if res is not None:
                        # print("pre append")
                        node = dll.append(res.content)
                        # print("post append")
                        if isinstance(res.content, Expr):
                            # print("pre pq")
                            pq.put((res.precedence, i, node))
                            # print("post pq")
                # print("after pq if")

        if listCondition is not None:
            dll.append(listCondition)
            listCondition = None

        print("pre loop dll size: " + str(dll.size))
        if dll.size != 0:
            while not pq.empty():
                curr = pq.get()[2]
                # print("processing: " + str(curr.data.operator))
                curr.data.operands = (curr.prev.data, curr.next.data)
                # print(curr.data.operands)
                dll.remove(curr.prev)
                dll.remove(curr.next)

            print("post loop dll size: " + str(dll.size))
            print(toDNF(dll.head.data))
    except Exception as e:
        print(e)
    return 1


def processText(text: str, flags: prereqScrapingFlags) -> processTextRes | None:
    # print("processing text")
    text = text.lower().strip()
    # print(text)

    if any(x in text for x in ("admission", "point", "provide")):
        # print("literal case")
        return processTextRes(content=Literal(code=False, content=text))
    elif "any of" in text or "one of" in text:
        if "admission" in text:
            # print("setting reading list")
            flags.readingList = True
            return processTextRes(
                precedence=None,
                content=Literal(code=False, content=text),
                firstInList=True,
            )
        else:
            # print('setting false')
            flags.readingList = False
            flags.andTableMode = False
            # print("any case")
            return None
    elif "both of" in text or "all of" in text:
        flags.readingList = False
        flags.andTableMode = True
        # print("all case")
        return None
    elif text == "and":
        # print("and case")
        flags.readingList = False
        return processTextRes(
            precedence=OpPrecedence.AND,
            content=Expr(operator=LogicOp.AND, operands=(None, None)),
        )
    elif text == "or":
        # print("or case")
        flags.readingList = False
        return processTextRes(
            precedence=OpPrecedence.OR,
            content=Expr(operator=LogicOp.OR, operands=(None, None)),
        )
    elif "option" in text and "option 1" not in text and "options" not in text:
        # print("option case")
        flags.readingList = False
        return processTextRes(
            precedence=OpPrecedence.OPTION,
            content=Expr(operator=LogicOp.OR, operands=(None, None)),
        )
    elif flags.readingList:
        return processTextRes(content=Literal(code=False, content=text))

    return None


def generateTableExpr(table: WebElement, flags: prereqScrapingFlags):
    # print("generating")
    if flags.andTableMode:
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

    flags.andTableMode = True
    return currExpr
