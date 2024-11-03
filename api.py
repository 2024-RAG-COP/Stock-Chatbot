from fastapi import FastAPI, File, UploadFile, Form
from gpt_assistant import *
from state import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/getCompanyAnalysis/")
async def getCompanyAnalysis(file: UploadFile = File(...), company: str = Form(...)):
    print(file.filename, company)

    return {"filename": file.filename}

@app.post("/getNextAnalysis/")
async def getNextAnalysis(phaseNum: str = Form(...)):
    print(phaseNum)
    return {"phaseNum": phaseNum}

@app.post("/retryAnalysis/")
async def retryAnalysis():
    print("retryAnalysis")

    return {"만들었다":"이녀석아"}

