from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()

model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite')


class State(TypedDict):
    title:str
    outline:str
    blog:str


def Name(State:State):
    title  =  State['title']
    prompt = f"take this tiitle {title} and develop the outline for the blog only outline not other words but have to be modern "
    result = model.invoke(prompt)
    
    final = result.content[0]['text']
    State['outline'] = final

    return State

def Dept(State:State):
    outline  = State['outline']
    prompt = f"take this outline {outline} and write 200 words blog , modern style, sharp and to the point with real world examples"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['blog']=final
    return State



graph = StateGraph(State)
graph.add_node('name_node',Name)
graph.add_node('dept_node',Dept)
graph.add_edge(START, 'name_node')
graph.add_edge("name_node" ,'dept_node')
graph.add_edge('dept_node' ,END)
workflow = graph.compile()
# initial = {'title':'Universe'}
# a = workflow.invoke(initial)
# print(a)


@app.post('/blog')
def get(title:str = Body(...)):
    initial = {'title':title}
    a = workflow.invoke(initial)
    return JSONResponse(status_code = 200, content = a)

