from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from typing import TypedDict,Literal
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    query:str
    budget:Literal['Low','Mid','High']
    response:str
class Budget(BaseModel):
    budget:Literal['Low','Mid','High']


app = FastAPI()


model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")


def analyze_node(State:State):
    query = State['query']
    prompt = f"Analyze and tell the budget profile of individual not based on salary based on budget and guests and others:{query}"
    models = model.with_structured_output(Budget)
    result = models.invoke(prompt)
    final = result.budget
    State['budget']=final

    return {'budget':final}


def condition(State:State):
    budget = State['budget']
    if budget=="Low":
        return "low_node"
    if budget=="Mid":
        return "mid_node"
    if budget=="High":
        return "high_node"









def low_node(State:State):
    query = State['query']
    budget=State['budget']
    prompt = f"You are agent for low budget:   This is the profile of usre {query} give the best wedding budget for him based on his profile"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['response']=final

    return State
def mid_node(State:State):
    query = State['query']
    budget=State['budget']
    prompt = f"You are agent for mid budget:  This is the profile of usre {query} give the best wedding budget for him based on his profile"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['response']=final

    return State
def high_node(State:State):
    query = State['query']
    budget=State['budget']
    prompt = f"You are agent for high budget:   This is the profile of usre {query} give the best wedding budget for him based on his profile"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['response']=final

    return State



graph = StateGraph(State)


graph.add_node("Analyze",analyze_node)
graph.add_node("low_node",low_node)
graph.add_node("mid_node",mid_node)
graph.add_node("high_node",high_node)


graph.add_edge(START,"Analyze")
graph.add_conditional_edges("Analyze",condition)
graph.add_edge("low_node",END)
graph.add_edge("mid_node",END)
graph.add_edge("high_node",END)



workflow= graph.compile()


@app.post('/get')
def func(item:str = Body(...)):


    initialState = {'query':item}

    final = workflow.invoke(initialState)
    return JSONResponse(status_code=200, content=final)

