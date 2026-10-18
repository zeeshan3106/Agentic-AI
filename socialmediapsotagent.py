from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import requests
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PYPDFLoader
from pymongo import MongoClient 
from langchain_mongodb import MongoDBAtlasVectorSearch


model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
app = FastAPI()
class State(TypedDict):
    query:str
    rag:Literal['yes','no']
    raged:str
    post:str
    fb:str
    insta:str
    linkedin:str
    final:str

def Rag(State:State):
    API = ""
    embedding = GoogleGenerativeAIEmbeddings(model = "")
    connect = MongoClient(API)
    database = connect['Database']
    collection = database['papersdata']
    db= MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name ="vector-index"
    )

    loader = PYPDFLoader(path = r"Australia Awards Scholarships 2027 (1).pdf")
    result = loader.laod()
    final = result[0].page_content
    db.add_texts([final])


def Raged(State:State):
    retrieved = db.as_retriever(
        search_kwargs  ={
            'k':1
        }

    )
    State['raged']=retrieved




def Post(State:State):
    query = State['query']
    raged = State['raged']
    prompt = f"{query} based on this query create a post for our youtube channel from this db{raged}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['post']=final
    return {
        'post':final
    }

def Facebook(State:State):
    post = State['post']
    raged = State['raged']
    prompt = f"take this post {post} and add the keywords and tags regardign our facebook history and relatesto this post and that trends and return full post from this db{raged} "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['fb']=final
    API  = ""
    payload={
        'fb':final
    }

    res = requests.post(API,payload)
    return {
        'fb':final
    }
def Instagram(State:State):
    post = State['post']
    raged = State['raged']
    prompt = f"take this post {post} and add the keywords and tags regardign our Instagram history and relatesto this post and that trends and return full post from this db{raged}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['insta']=final
    API  = ""
    payload={
        'insta':final
    }

    res = requests.post(API,payload)
    return {
        'insta':final
    }

def Linkedin(State:State):
    post = State['post']
    raged = State['raged']
    prompt = f"take this post {post} and add the keywords and tags regardign our Linkedin history and relatesto this post and that trends and return full post from this db{raged}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['linkedin']=final
    API  = ""
    payload={
        'Linkedin':final
    }

    res = requests.post(API,payload)
    return {
        'linkedin':final
    }
def Final(State:State):
    fb= State['fb']
    insta = State['insta']
    linkedin = State['linkedin']
    fb = len(fb)
    insta = len(insta)
    linkedin = len(linkedin)
    if fb > 0 and insta > 0 and linkedin > 0:
        prompt = f" all posts are successfully created and deployed on accounts(fb,insta,linkedin) create a greeting message for user"
        result = model.invoke(prompt)
        final = result.content[0]['text']
        State['final']=final
    return State
    


def condition(State:State):
    rag  = State['rag']
    if rag == 'yes':
        return 'rag'
    else:
        return 'raged'




graph = StateGraph()
graph.add_node('rag',Rag)
graph.add_node('raged',Raged)
graph.add_node('post',Post)
graph.add_node('fb',Facebook)
graph.add_node('instagram',Instagram)
graph.add_node('linkedin',Linkedin)
graph.add_node('final',Final)
graph.add_edge(START, condition)
graph.add_edge('raged','post')
graph.add_edge('post','fb')
graph.add_edge('fb','instagram')
graph.add_edge('instagram','linkedin')
graph.add_edge('linkedin','final')
graph.add_edge('final',ENd)
graph.add_edge('rag',END)
connect = sqlite3.connect(database="ABC", check_same_thread=False)
checkpointer = SqliteSaver(connect)
config = {'configurable':{'thread_id':1}}


@app.post('/agent')
def Agent(Data:str = Body(...)):
    workflow = graph.compile(checkpointer=checkpointer)
    # initial_state={'query':'create post regarding ai workflows the core components of ai workflows almost 1000 words technical parts as well'}
    initial_state = {
        'query':Data
    }
    final = graph.compile(initial_state, config = config)
    return JSONResponse(
        status_code = 200,
        content = final
    )
