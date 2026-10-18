from langgraph.graph import StateGraph, START,END
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from typing import TypedDict, Literal
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymonogo import MongoClient
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()
model = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")
embedding = GoogleGenerativeAIEmbeddings()
app  = FastAPI()
API = ""
client = MongoClient(API)

class State(TypedDict):
    query:str
    analyze:Literal['color','price','basic','platform','storage','battery','design','display','network','camera','camera','media','connectivity','location','sensors']
    color:str
    price:str
    basic:str
    platform:str
    storage:str
    battery:str
    design:str
    display:str
    network:str
    camera:str
    media:str
    connectivity:str
    location:str
    sensors:str

class Analyzig(TypedDict):
     analyze:Literal['color','price','basic','platform','storage','battery','design','display','network','camera','camera','media','connectivity','location','sensors']
   




def Analyze(State:State):
    query = State['query']
    prompt = f" thisis the query of the individual only analyze that this quey is relates to which of thsi field query:stranalyze:Literal['color','price']color:strprice:strbasic:strplatform:strstorage:strbattery:strdesign:strdisplay:strnetwork:strcamera:strmedia:strconnectivity:strlocation:strsensors:str"
    model = model.with_structured_output(Analyzig)
    result = model.invoke(prompt)
    State['analyze']=result['analyze']

def Color(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['Color']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag that have these colors must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['color']=final

def Price(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['Price']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have these price must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['price']=final



def Basic(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['Basic']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have these basics must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['basic']=final


def Platform(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['platform']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have these platforms must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['platform']=final


def Storage(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['storage']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have these storage must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['storage']=final

def Battery(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['storage']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have these storage must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['storage']=final

def Design(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['design']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked design must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['design']=final


def Display(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['display']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked display must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['display']=final

def Network(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['network']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked network must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['network']=final

def Camera(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['camera']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked camera must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['camera']=final

def Media(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['network']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked network must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['network']=final


def Connectivity(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['connectivity']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked Connectivity must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['connectivity']=final

def Location(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['location']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked location must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['location']=final

def Sensors(State:State):
    query = State['query']
    database = client['Mobile']
    collection = database['sensors']
    db = MongoDBAtlasVectorSearch(
        embedding= embedding,
        collection=collection,
        index_name='vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            k:'20'
        }
    )
    result = retriever.invoke(query)

    prompt = f"Based on this {query} give the 10 mobiles from our rag{result} that have top ranked sensors must and same compay user want"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['sensors']=final






graph = StateGraph()

graph.add_node('analyze',Analyze)
graph.add_node('color',Color)
graph.add_node('price',Price)
graph.add_node('basic',Basic)
graph.add_node('platform',Platform)
graph.add_node('storage',Storage)
graph.add_node('battery',Battery)

graph.add_edge(START, 'analyze')
graph.add_edge('analyze','color')
graph.add_edge('color','price')
graph.add_edge('price','basic')
graph.add_edge('basic','platform')
graph.add_edge('platform','storage')
graph.add_edge('storage','battery')
graph.add_edge('battery',END)

connect  = sqlite3.connect(database = "ABC", check_same_thread=False)
checkpointer = SqliteSaver(connect)

worlflow = graph.compile(checkpointer=checkpointer)
config = {'configurable':{'thread_id':1}}
@app
def API(query:str = Body(...)):
    initial_state = {'query':query}
    
    final = workflow.invoke(initial_state)