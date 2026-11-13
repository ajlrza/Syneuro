from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from . import brain
import json

# Server 

origins = [
    "",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_methods=["*"],             
    allow_headers=["*"],             
)

@app.post("/live_talk")
async def read_request(request: Request):

    body = await request.json()
    body = body or {}


    api_response = brain.syneuro_inference

    if api_response is False:
        pass

    return api_response.get('Response')


@app.post("/saveData")
async def read_request(request: Request):
    
    body = await request.json()

    data_mode = {
        "Text": "",
        "Audio": "",
        "Image": "",
        "Video": "",
        "Sensory": ""
    }

    payload = ""

    with open("python_javascript_bridge.json", "w", encoding="utf-8") as File:
        json.dump(payload, File)

@app.post("/loadData")
async def read_request(request: Request):

    body = await request.json()


    # Return stored data for the given user if available
    # THIS ONE SOON
    try:
        with open("bridge.json", "r", encoding="utf-8") as File:
            data = json.load(File)
    except FileNotFoundError:
        data = {}
    return data


@app.post("/loadMemory")
async def read_request(request: Request):

    body = await request.json()

    try:
        with open("python_javascript_bridge.json", "r", encoding="utf-8") as File:
            data = json.load(File)
    except FileNotFoundError:
        data = {}
    return data

@app.post("/test")
async def read_request(request: Request):

    body = await request.json()

    requestReq = body.get("Test")
    return requestReq
