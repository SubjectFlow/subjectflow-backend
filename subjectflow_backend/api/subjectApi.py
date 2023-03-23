from pymongo import database, UpdateOne
from subjectflow_backend.models.subject import Subject, UpdateSubject
from fastapi.encoders import jsonable_encoder

SUB_COLL = "subjects"


async def dropAllSubjects(db: database):
    try:
        db[SUB_COLL].drop()
    except Exception as e:
        print(e)
        return error(e)


async def postSubject(db: database, subject: Subject):
    try:
        return db[SUB_COLL].insert_one(jsonable_encoder(subject))
    except Exception as e:
        print(e)
        return error(e)


async def postSubjects(db: database, subjects: list[Subject]):
    try:
        docs = map(lambda x: jsonable_encoder(x), subjects)
        return db[SUB_COLL].insert_many(docs)
    except Exception as e:
        print(e)
        return error(e)


async def getSubjectByCode(db: database, code: str):
    try:
        return db[SUB_COLL].find_one({"code": code})
    except Exception as e:
        print(e)
        return error(e)


async def updateSubjectByCode(db: database, code: str, subject: UpdateSubject):
    try:
        return db[SUB_COLL].update_one({"code": code}, jsonable_encoder(subject))
    except Exception as e:
        print(e)
        return error(e)


async def updateSubjectsByCode(
    db: database, updateReqs: list[tuple[str, UpdateSubject]]
):
    try:
        req: list[UpdateOne] = map(
            lambda x: UpdateOne({"code": x[0]}, jsonable_encoder(x[1])), updateReqs
        )
        return db[SUB_COLL].update_many(req)
    except Exception as e:
        print(e)
        return error(e)


def error(e):
    return {"err": e}
