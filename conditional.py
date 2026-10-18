from langgraph.graph import StateGraph,START, END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

os.environ['LangSmith_project']="ABC"

class State(TypedDict):
    query:str
    service:Literal['restaurant','hotel','dentist']
    restaurant:str
    hotel:str
    dentist:str




class Service(TypedDict):
    service:Literal['restaurant','hotel','dentist']

class Restaurant(TypedDict):
    restaurant:str


class Hotel(TypedDict):
    hotel:str


class Dentist(TypedDict):
   dentist:str





def SelectServce(State:State):
    query = State['query']
    prompt = f"This is the query understand it reason it and tell me the service user want"
    model = model.with_structured_output(Service)
    result = model.invoke(prompt)
    State['service']=result['service']

def Restaurant(State:State):
    service = State['service']
    prompt = f"Book top ranked restaurant in california "
    model = model.with_structured_output(Restaurant)
    result = model.invoke(prompt)
 
    return {
        'restautant':result
    }

def Dentist(State:State):
    service = State['service']
    prompt = f"Book top ranked Dentist in california "
    model = model.with_structured_output(Dentist)
    result = model.invoke(prompt)
    State['dentist']=result
 
    return {
        'dentist':result
    }

def Hotel(State:State):
    service = State['service']
    prompt = f"Book top ranked Hotel in california "
    model = model.with_structured_output(Hotel)
    result = model.invoke(prompt)
    State['hotel']=result
 
    return {
        'hotel':result
    }


def condition(State:State):
    service = State['service']
    if service == 'restaurant':
        return 'restaurant'
    elif service== 'hotel':
        return 'hotel'
    elif service == 'dentist':
        return 'dentist'




graph = StateGraph(State)

graph.add_node('selectservce',SelectServce)
graph.add_node('restaurant',Restaurant)
graph.add_node('hotel',Hotel)
graph.add_node('dentist',Dentist)

graph.add_edge(START, 'selectservce')
graph.add_conditional_edges('selectservce', condition)
graph.add_edge('restaurant',END)
graph.add_edge('hotel',END)
graph.add_edge('dentist',END)



checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)
config = {'configurable':{'thread_id':1}}

initial_state = {'query','I want to book for stay in San Fransisco'}
final = workflow.invoke(initial_state, config=config)


workflow.get_state(config)
list(workflow.get_state_history())
print(final)
