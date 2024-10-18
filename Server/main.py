from fastapi import FastAPI
import requests
import json
from reportlab.lib.pagesizes import letter
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def getAccess_token():
    url = 'https://id.trimble.com/oauth/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic base64string'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'trimble-global-hack-2024'
    }
    response = requests.post(url, headers=headers, data=data)
    access_token = response.json()['access_token']
    print(access_token)
    return access_token


def get_response_msg(message:str,token:str):
    print(token)
    url = "https://agw.construction-integration.trimble.cloud/trimbledeveloperprogram/assistants/v1/agents/hackmanual/messages"
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    request_body = {
        "message": message,
        "session_id": "1",
        "stream": False,
        "model_id": "gpt-4"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(request_body))
        print(response.json())
        return response.json()['message']
    except Exception as e:
        print(e)

@app.get("/message")
def read_root():
    access_token = getAccess_token()
    return access_token

@app.get("/generateResponse/{req}")
def qa_with_gpt(req:str):
    token = getAccess_token()
    response = get_response_msg(req,token)
    return response




