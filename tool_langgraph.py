from langgraph.graph import StateGraph,START, END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.tools import tool
from langchain_core.tools import DuckDuckGoSearchRun
import requests
import json
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.1-flahs-lite")


class State(TypedDict):
    query:str
    tool:str
    tooltwo:str
    live:str
    status:Literal['live','llm']



class Status(TypedDict):
    status:Literal['live','llm']



@tool
def Add(name:str,email:str,service:str):
    payload = {
        'name':name,
        'email':email,
        'service':service
    }
    API=''
    res = requests.post(API,payload)
    final = res.json()
  


def Analyze(State:State):
    query = State['query']
    prompt = f"Based on this query should ans this our llm or it should be live "
    model = model.with_structured_output(Status)
    result = model.invoke(prompt)
    State['status']=result['status']




def LiveDataTool(State:State):
    query = State['query']
    search = DuckDuckGoSearchRun()
    result = search.invoke(query)
    State['live']=result
    return {
        'live':result
    }




def Decision(State:State):
    query = State['query']
    prompt = f"{query} if query consisted of Name email, and servce run add tool"
    model = model.bind_tools([Add])
    result = model.invoke(prompt)
    final = result.content[0]['text']

def condition(State:State):
    status = State['status']

    if status== 'live':
        return 'live'
    else:
        return 'decision'





graph  = StateGraph()

graph.add_node('decision',Decision)
graph.add_node('analyze',Analyze)
graph.add_node('live',LiveDataTool)


graph.add_edge(START,'analyze')
graph.add_edge('analyze',condition)
graph.add_edge('decision',END)
graph.add_edge('live',END)

connect = sqlite3.connect(database='abc', check_same_thread=False)
checkpointer = SqliteSaver(connect)
config = {'configurable':{'thread_id':1}}
workflow = graph.compile(checkpointer=checkpointer)
initial_state={'query':'Name is Zeeshan email zeeshanalizafar53, serivce is bracing'}
final = workflow.invoke(initital_state, config = config)

workflow.get_state(config)
print(list[workflow.get_state_history()])
