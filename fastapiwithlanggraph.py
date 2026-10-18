from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import json


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
class State(TypedDict):
    query:str
    result:str


def Result(State:State):
    query= State['query']
    prompt = f"{query} this is the quer from user ans this from your parametric knowledge"
    result = model.invoke(prompt)
    final = result.content[0]['text']

    State['result']=final
    return State


graph = StateGraph()

connect = sqlite3.connect(database="ABC",check_same_thread=False)
checkpointer=SqliteSaver(connect)
workflow = graph.compile(checkpointer=checkpointer)



@app.post('/get')
def ITem(Data:str = Body(...)):
    
    initial_state=Data
    final = workflow.invoke(initial_state)

    return JSONResponse(status_code=200,content=final)

        

