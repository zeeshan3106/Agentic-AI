from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import requests
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from pymongo import MongoClient
from langchain_mogdodb import MongoDBAtlasVectorSearch
from langchain_community.tools import tool
from send import EmailSend
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class State(TypedDict):
    query:str
    booking:Literal['yes', 'no']
    raged:str
    final:str

    



@tool
def Booking(name:str,
    email:str,
    dept:str,
    service:str,
    specialist:str,
    time:str,
    desc:str):

    payload = {
        'name':name,
        'email':email,
        'dept':dept,
        'service':service,
        'specialist':specialist,
        'time':time,
        'description':desc
    }
    APi = ""
    res  = requests.post(API, payload)
    a = EmailSend(
                to_email=email
                , name=name
                ,contact = contact
                ,service=service,
                time=time

            )
    prompt = f"this{payload} is the booking of the user create summary for it.emai also sent successfully"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final




    


def Rag(State:State):
    API = ""
    embedding = GoogleGenerativeAIEmbeddings(model = "")
    connect = MongoClient(API)
    database = connect['database']
    collection = database['mthc']
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    db.add_texts([])

def Raged(State:State):
    query = State['query']
    result = db.as_retriever(
        search_kwargs = {
            'k':2
        }
    )
    final = result.invoke(query)
    State['raged']=final


def Model(State:State):
    query = State['query']
    raged = State['raged']
    model = model.bind_tools([Booking])
    prompt = f" This is the query{query} ans the user from this db{raged} when user specifically said i want to do booking or wana do booking for booing and the info of all elements are provided run the Booking tool otherwise no"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final
    return State


graph = StateGraph()
graph.add_node('rag',Rag)
graph.add_node('raged',Raged)
graph.add_node('model',Model)
graph.add_edge(START, condition)
graph.add_edge('raged','model')
graph.add_edge('model',Model)

connect = sqlite3.connect(database="ABC", check_same_thread=False)
checkpointer = SqliteSaver(connect)

workflow = graph.compile(checkpointer = checkpointer)
config = {'configurable':{'thread_id':1}}

@app.post('/agent')
def Agent(Data:str=Body(...)):

    initial_state={'query':Data}
    final = workflow.invoke(initial_state, config = config)






