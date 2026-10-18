from langgraph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import requests
from dotenv import load_dotenv
import json
from dotnev import load_dotenv

load_dotenv()
model =ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
embedding = GoogleGenerativeAIEmbeddings(model = "")
app = FastAPI()

class State(TypedDict):
    task:str
    grammer:str
    advance_vocab:str
    book:int
    exercise:int
    taskno:int
    band:float
    optimize_task:str
    history:list


class IELTSBand(TypedDict):
    band:Literal[4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9]


payload = {
        'book':State['book'],
         'exercise':State['exercise'],
         'task':State['taskno']
    }
res = requests.get(API, payload)
original = res.json()



def Grammer(State:State):
    task = State['task']
    prompt = f" {task} this is the task of ielts writing only check grammer mistakes and list all mistakes each an every from this essay to a list in end also total count of that mistakes  "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['grammer']=final
    return {
        'grammer':final
    }

def Vocab(State:State):
    task = State['task']
    prompt = f"{task} this is the task se same setences just replace the words to needed vocabuary to make it band 8 or 9 task liek Human not AI"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['advance_vocab']=final
    return {
        'advance_vocab':final
    }


def Band(State:State):


    task = State['task']
    prompt = f"{task} this is the task strictly check and give it a band of IELTs Academic from 5 - 9 float based on this original task{original}"
    model = model.with_structured_output(IELTSBand)
    result = model.invoke(prompt)
    
    State['band']=result['band']
    return {
        'band':result['band']

    }


def Optimized(State:State):
    task = State['task']
    prompt = f" this is the task {task} written by user and this is the original one {original} write this task that i have written based on the orginal one for band 9 like human not AI"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['optimize_task']=final

    return {
        'optimize_task':final
    }


def Summary(State:State):
    history=State['history']
    task = State['task']
    prompt = f" this is the history {history} and this is the today task {task} and original {original} create a summary by bands for all in table and also demonstrate that do our overall perfeormance in terms of vocab and advance sentences our not model generated the our task is increasing on decreasing? "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final
    return 
    


def condition(State:State):
    band = State['band']
    if band > 8:
        return 'optimize'
    else:
        return 'summary'


graph = StateGraph()

graph.add_node('grammer',Grammer)
graph.add_node('vocab',Vocab)
graph.add_node('band',Band)
graph.add_node('optimize',Optimized)
graph.add_node('summary',Summary)
graph.add_edge(START, 'grammer')
graph.add_edge('grammer','vocab')
graph.add_edge('vocab','band')
graph.add_conditional_edges('band', condition)
graph.add_edge('optimize',END)
graph.add_edge('summary',END)

connect = sqlite3.connect(database="IELTS", check_same_thread=False)
checkpointer = SqliteSaver(connect)
workflow = graph.compile(checkpointer = checkpointer)
config = {'configurable':{'thread_id':1}}
history = list[workflow.get_state_history]


@app
def IELTSTask(task:dict= Body(...)):

    initial_state = {
    'task':task['task'],
    'book':task['book'],
    'exercise':task['exercise'],
    'taskno':task['taskno'],
    'history':history
    }
    final = workflow.invoke(initial_state, config = config)
    return JSONResponse(
        status_code = 200,
        content = final
    )




