from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
from pymongo import MongoClient
from langchain_mogdodb import MongoDBAtlasVectorSearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
import requests
import sqlite3
from dotenv import load_dotenv
from langchain_community.tools import tool
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import json
load_dotenv()


class State(TypedDict):
    query:str
    raged:Literal['yes','no']
    rag:str
    result:str
    add:str
    update:str
    delete:str
    mail_status:Literal['add','delete','update','no']
    email:str

class Mail(TypedDict):
    mail_status:Literal['add','delete','update','no']



model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
API=""
embedding = GoogleGenerativeAIEmbeddings(model = "")
connect = MongoClient(API)
database = connect['Database']
collection = database['restaurantdata']
db = MongoDBAtlasVectorSearch(
    embedding = embedding,
    collection = collection,
    index_name = 'vector_index'

)

@tool
def Addtool(name:str,contact:str,email:str,dish:dict,time:str):
    payload={
        'name':name,
        'contact':contact,
        'email':email,
        'dish':dish,
        'time':time
    }
    API = ""
    res = requests.post(API,payload)
    final = res.json()
    State['add']=final
    a = EmailSend(
                to_email=email
                , name=name
                ,contact = contact
                ,dishes=dish,
                time=time

            )


@tool
def Deletetool(name:str,dish:dict,email:str,time:str):
    payload={
        'name':name,
        'email':email,
        'time':time
    }
    API = ""
    res = requests.delete(API,payload)
    final = res.json()
    State['delete']=final
    a = EmailSend(
                to_email=email
                , name=name
                ,contact = ''
                ,dishes='',
                time=time

            )
@tool
def Updatetool(name:str,dish:dict,email:str,time:str):
    payload={
        'name':name,
        'email':email,
        'time':time,
        'dish':dish
    }
    API = ""
    res = requests.put(API,payload)
    final = res.json()
    State['update']=final
    a = EmailSend(
                to_email=email
                , name=name
                ,contact = ''
                ,dishes=dish,
                time=time

            )







def Raged(State:State):
    loader = TextLoader(
        path=r"C:\Users\cb\Desktop\Practice Langgraph\rag.txt"
    )
    result = loader.load()
    final = result[0].page_content
    db.add_texts([final])



def Rag(State:State):
    query = State['query']
    
    rag = db.as_retriever(
        search_kwargs={'k':2}
    )
    State['rag']=rag
    return {
        'rag':rag
    }


def Model(State:State):
    query = State['query']
    rag = State['rag']
    model = model.bind_tools([Addtool,Deletetool,Updatetool])
    prompt = f"{query} this is the query and this is the Rag {rag}butify it and provide each single info to user if user say he wasnt to do book ask for name,email,contact,dishes and time when all of these avaiable only then run AddTool,  ony when user say he wasnt tto update the data ask for name, email adn time and run update tool wen you have info,     when user say i want to cancel booking /delte record ask for name,email and time and run DeleteTool  "
    result = model.invoke(prompt)
    if result.tool_calls:
        tool = result.tool_calls[0]
        if tool['name']=='AddTool':
            State['mail_status']='add'

        if tool['name']=='DeleteTool':
            State['mail_status']='delete'
        if tool['name']=='UpdateTool':
            State['mail_status']='update'
    else:
        State['mail_status']='no'
    final = result.content[0]['text']
    State['result']=final
    return State

def condition(State:State):
    raged=State['raged']

    if raged == "yes":
        return 'raged'
    else:
        return 'retriever'


graph = StateGraph()
graph.add_node('raged',Raged)
graph.add_node('retriever',rag)
graph.add_node('model',Model)
graph.add_conditional_edges(START, condition)
graph.add_edge('retriever','model')
graph.add_edge('model',END)
graph.add_edge('raged',END)
connect = sqlite3.connect(database="ABC",check_same_thread=False)
checkpointer = SqliteSaver(connect)
workflow = graph.compile(checkpointer=checkpointer)
config = {'configurable':{'thread_id':1}}
@app.post('/agent')
def Agent(Data:str=Body(...)):

    initial_state={'query':Data}
    final = workflow.invoke(initial_state, config = config)
    return JSONResponse(status_code=200, content=final)



