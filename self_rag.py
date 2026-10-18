from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
import os
os.environ['LangSmith_Project']="New Name"
model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
load_dotenv()
class State(TypedDict):
    query:str
    status:Literal['general','rag']
    general:str
    rag:str
    relevant:Literal['yes','no']
    relevant_category:Literal['full','partial','not']
    optimized:str
    final:str
    optimized_query:str
    notfound:str

class Status(TypedDict):
    status:Literal['general','rag']
   
class Relevant(TypedDict):
    relevant:Literal['yes','no']
    
class Relevant_category(TypedDict):
    relevant_category:Literal['full','partial','not']
    
 



def Analyze(State:State):
    query = State['query']
    prompt = f"take this query and check that it could be answered from parametric knowledge or only its a rag one "
    model = model.with_structured_output(Status)
    result = model.invoke(prompt)
    State['status']=result['status']


def General(State:State):
    query = State['query']
    result = model.invoke(query)
    final = result.content[0]['text']
    State['general']=final
    return State


def Retriver(State:State):
    query = State['query']
    result = db.as_retriever(search_kwargs={'k':2})
    final = result.page_content
    State['rag']=final


def Relevant(State:State):
    query = State['query']
    rag = State['rag']
    prompt = f"check is the result {rag} is relevant with the query{query}"
    model = model.with_structured_output(Relevant)
    result = model.invoke(prompt)
    State['relevant']=result['relevant']
    prompt = f"Give tis is fully,partially or no relevant "
    model = model.with_structured_output(Relevant_category)
    result = model.invoke(prompt)   
    State['relevant_category']=result['relevant_category']




def optimization(State:State):
    query:State['query']
    rag:State['rag']
    prompt = f"this is the rag for this query maeke it optiize to answer it fully if you can via parametric knowledge"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['rag']=final

def Requery(State:State):
    query = State['query']
    rag=State['Rag']
    prompt = f"this is the query{query} and the result is coming is this {rag} but its not fulfilling the users ans rearrage the query to be retireved from db only query no other word"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['query']=final


def NotFound(State:State):
    query = State['query']
    prompt = f"for this query{query} result not found give user the message"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['notfound']=final

    return State


def Final(State:State):
    query = State['query']
    rag = State['rag']
    prompt = f"This{rag} is the final 100% releveant result of this query{query} butify it perfectly"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final



def condition(State:State):
    status = State['status']

    if status== "rag":
        return 'retriever'
    else:
        return 'general'

def Condition(State:State):
    relevant = State['relevant']
    relevant_category=State['relevant_category']

    if relevant == 'yes':
        if relevant_category=='full':
            return 'final'
        if relevant_category== 'partial':
            return 'optimize'
        if relevant_category=='not':
            return 'requery'
    else:
        return 'notfound'



graph = StateGraph()

graph.add_node('analyze',Analyze)
graph.add_node('general',General)
graph.add_node('retriever',Retriver)
graph.add_node('relevant',Relevant)
graph.add_node('optimize',optimization)
graph.add_node('requery',Requery)
graph.add_node('notfound',NotFound)
graph.add_node('final',Final)

graph.add_edge(START, 'analyze')
graph.add_conditional_edges('analyze',condition)
graph.add_edge('general',END)
graph.add_edge('retriever','relevant')
graph.add_conditional_edges('relevant', Condition)
graph.add_edge('final',END)
graph.add_edge('optimize','relevant')
graph.add_edge('requery','retriever')
graph.add_edge('notfound',END)


connect = sqlite3.connect(database="Apple", check_same_thread=False)
checkpointer = SqliteSaver()
config = {'configurable':{'thread_id':1}}
workflow=graph.compile(checkpointer=checkpointer)
initial_state={'query':'What is the time for dentist Stephen?'}
final = workflow.invoke(initial_state, config = config)
print(final)



