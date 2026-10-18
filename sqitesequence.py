from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import requests
import sqlite3


model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
class State(TypedDict):
    query:str
    plan:str
    dental:str
    name:str
    service:str
    cost:int
    contact:str
    booked:str

class Detail(TypedDict):
    name:str

    dental:str
    service:str
    cost:int
    contact:str




def alldentals(State:State):

    query = State['query']
    data = ""
    prompt = f"This is query of user make a plan for his visit to dentsit get all data about services from here {data}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['plan']=final
    return {
        'plan':final
    }


def selecteddental(State:State):
    plan = State['plan']
    prompt = f"rank the best dental from {plan} and give its services based on this query the user want {query}"
    model = model.with_structured_output(Detail)
    result = model.invoke(prompt)
    State['dental']=result['dental']
    State['service']=result['service']
    State['cost']=result['cost']
    State['contact']=result['contact']



def bookdental(State:State):
  
    eleements:{
        'name':State['name'],
        'service':State['service'],
        'cost':State['cost'],
        'contact':State['contact']
    }

    requests.post(API, eleements)



graph = StateGraph(State)

graph.add_node('alldentals',alldentals)
graph.add_node('selecteddental',selecteddental)
graph.add_node('bookdental',bookdental)


graph.add_edge(START,'alldentals')
graph.add_edge('selecteddental','bookdental')
graph.add_edge('bookdental',END)
connect= sqlite3.connect(database="Apple",check_same_thread=False)
checkpointer=SqliteSaver(connect)

workflow = graph.compile(checkpointer=checkpointer)

config = {'configurable':{'thread_id':1}}
initital_state={'query':'I wana book dental service in San Fransisco,My name is JD'}
final = workflow.invoke(initital_state, config=config)

workflow.get_state(config)
list(workflow.get_state_history())
print(final)
















    
