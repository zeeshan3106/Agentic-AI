from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()
os.environ['LangSmith_Project']="New Name"

model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite')

class State(TypedDict):
    query:str
    post:str
    rate:int
    revised:str
    final:str

class Rating(TypedDict):
    rate:int



def Create(State:State):
    query = State['query']
    prompt = f"Write a post of linkedin focused based on requirements of user{query}"
    result = model.invoke(prompt)
    final  = result.content[0]['text']
    State['post']=final

def Analyze(State:State):
    post = State['post']
    prompt=f"this is the post give it a rating between 1-10"
    model = model.with_structured_output(Rating)
    result = model.invoke(prompt)
    State['rate']=result['rate']

def revised(State:State):
    post=State['post']
    prompt = f"Revise this post and make it more sharper{post}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['post']=final

def Final (State:State):
    post=State['post']
    prompt = f"The Linkedin post is generated successfully make greeting message for client"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final
    return State


def condition(State:State):
    rate = State['rate']
    if rate > 8:
        return 'final'
    else:
        return 'optimization'
        

graph.add_node('create',Create)
graph.add_node('analyze',Analyze)
graph.add_node('revise',revised)
graph.add_node('final',Final)


graph.add_edge(START, 'create')
graph.add_edge('create','analyze')
graph.add_conditional_edges('analyze',condition)
graph.add_edge('revise','analyze')
graph.add_edge('final',END)

connect = sqlite3.connect(database="ABC", check_same_thread=False)
checkpointer = SqliteSaver(connect)
workflow=graph.compile(checkpointer=checkpointer)
config = {'congigureable':{'thread_id':1}}
initial_state={'query':'Give me Linkedin post on transformer architecture'}
final = workflow.invoke(initial_state, config=config)

workflow.get_state(config)
list(workflow.get_state_history())





