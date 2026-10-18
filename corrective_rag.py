from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
import os 


os.environ['LangSmith_Project']="New Name"


load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")

class State(TypedDict):
    query:str
    status:Literal['general', 'rag']
    general:str
    retrieved:str
    final:str
    notfound:str
    relevant:Literal['yes','no']

class Analyze (TypedDict):
    status:Literal['general', 'rag']

class Relevant():
    relevant:Literal['yes','no']

def Analyze (State:State):
    query = State['query']
    prompt = f"Analyze this query{query} and tell is this coud be answered from Rag knowlwdge or paramteric knowlwdge"
    model = model.with_structured_output(Analyze)
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['status']=final


def General(State:State):
    query = State['query']
    result = model.invoke(query)
    final = result.content[0]['text']
    State['general']=general
    return State


def Retrieve(State:State):
    query = State['query']
    ragd=db.as_retriever(
        search_kwargs={'k':'2'}
    )
    State['retrieved']=ragd.page_content



def RelevantStatus(State:State):
    query - State['query']
    retrieved = State['retrieved']
    prompt = f"Ana;yze is the retrieved result{retrieved} is highly relevant to query{query} "
    model = model.with_structured_output(Relevant)
    result = model.invoke(prompt)
    State['relevant']=result['relevant']

def NotFound(State:State):
    query = State['query']
    prompt = f"regarding this query {query} we didnot have any data in RAg say to user info not found"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['notfound']=final
    return State


def Final (State:State):
    query = State['query']
    retrieved = State['retrieved']
    prompt = f"based on this query{query} tis is the result beutify it{retrieved} "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final
    return State





def condition(State:State):
    status = State['status']

    if status == 'rag':
        return 'retrieve'
    else:
        return 'general'


def Condition(State:State):
    relevant = State['relevant']

    if relevant == 'yes':
        return 'final'
    else:
        return 'notfound'



graph = StateGraph()

graph.add_node('analyze',Analyze)
graph.add_node('general',General)
graph.add_node('retrieve', Retrieve)
graph.add_node('relevant', Relevant)
graph.add_node('notfound',NotFound)
graph.add_node('final',Final)

graph.add_edge(START,'analyze')
graph.add_conditional_edges('analyze',condition)
graph.add_edge('general',END)
graph.add_edge('retrieve','relevant')
graph.add_conditional_edges('relevant',Condition)
graph.add_edge('notfound',END)
graph.add_edge('final',END)


connect = sqlite3.connect(database="Apple", check_same_thread=False)
checkpointer = SqliteSaver()
config = {'configurable':{'thread_id':1}}
workflow = graph.compile(checkpointer=checkpointer)
initial_state={"query":"What are the openig hours of dental service?"}
final = workflow.invoke(initial_state, config=config)




workflow.get_state(config)
print(list[workflow.get_state_history()])




