from pymongo import database
from subjectflow_backend.models.subject import Subject
from fastapi.encoders import jsonable_encoder

SUB_COLL = "subjects"
ERR_MSG = "An error occurred"
ERR = {"err": ERR_MSG}


async def dropAllSubjects(db: database):
    try:
        await db[SUB_COLL].drop()
    except:
        return


async def postSubject(db: database, subject: Subject):
    try:
        return await db[SUB_COLL].insert_one(jsonable_encoder(subject))
    except:
        return ERR


async def postSubjects(db: database, subjects: list[Subject]):
    res = []
    for subject in subjects:
        res.append(await postSubject(db=db, subject=subject))

    return res


async def getSubjectByCode(db: database, code: str):
    try:
        return await db[SUB_COLL].find_one({code: code})
    except:
        return ERR
