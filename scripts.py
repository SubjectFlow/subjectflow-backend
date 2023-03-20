import uvicorn

def server():
    uvicorn.run("subjectflow_backend.main:app")