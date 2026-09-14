from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI , Body
from fastapi.responses import JSONResponse

load_dotenv()
model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")
app = FastAPI()

class State(TypedDict):
    problem:str
    cause:str
    resolving:str
    tone:Literal['beautiful', 'aggresive', 'normal']
    urgency:Literal['low', 'mid', 'high']
    Summary:str



class toneSchamea(BaseModel):
    tone:Literal['beautiful', 'aggresive', 'normal']

class UrgencySchamea(BaseModel):
    urgency:Literal['low', 'mid', 'high']



def cause_node(State:State):
    problem=State['problem']
    prompt = f"give me cause of this problem only cause no other 5 lines max{problem}"
    result = model.invoke(prompt)
    cause = result.content[0]['text']
    State['cause']=cause

    return {'cause':cause}

def resolve_node(State:State):
    problem=State['problem']
    prompt = f"give me solution of this problem only no other{problem}"
    result = model.invoke(prompt)
    resolving = result.content[0]['text']
    State['resolving']=resolving

    return {'resolving':resolving}
def tone_node(State:State):
    problem=State['problem']
    prompt = f"give me tone of this problem only c no other{problem}"

    models = model.with_structured_output(toneSchamea)
    result = models.invoke(prompt)
    tone = result.tone
    State['tone']=tone

    return {'tone':tone}
def urgency_node(State:State):
    problem=State['problem']
    prompt = f"give me urgency of this problem only no other{problem}"
    modeler = model.with_structured_output(UrgencySchamea)
    result = modeler.invoke(prompt)
    urgency=result.urgency
    State['urgency']=urgency

    return {'urgency':urgency}

def summary_node(State:State):
    results = []
    problem=State['problem']
    results.append(problem)
    cause=State['cause']
    results.append(cause)
    resolve=State['resolving']
    results.append(resolve)
    tone=State['tone']
    results.append(tone)
    urgency=State['urgency']
    results.append(urgency)

    
    prompt = f"Make it final Summary{results}"
    result = model.invoke(prompt)
    
    summary=result

    return State





graph = StateGraph(State)

graph.add_node('cause',cause_node)
graph.add_node('resolve',resolve_node)
graph.add_node('tone',tone_node)
graph.add_node('urgency',urgency_node)
graph.add_node('summary',summary_node)


graph.add_edge(START, 'cause')
graph.add_edge(START, 'resolve')
graph.add_edge(START, 'tone')
graph.add_edge(START, 'urgency')

graph.add_edge('cause','summary' )
graph.add_edge('resolve','summary' )
graph.add_edge('tone', 'summary')
graph.add_edge('urgency', 'summary')

graph.add_edge('summary',END)




@app.post('/get')
def Assist(initial_states:str = Body(...)):
    workflow = graph.compile()
    initial_state={'problem':initial_states}
    a = workflow.invoke(initial_state)
    return JSONResponse(status_code = 200, content = a)

