from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class State(TypedDict):
    query:str
    blog:str
    rate:int
    optimized:str
    final:str
    modelfinal:str
    iteration:int
class Rate(TypedDict):
    rating:Literal[1,2,3,4,5,6,7,8,9,10]


def CreateBlog(State:State):
    query = State['query']
    prompt = f"This is the user query give the blog with this title and outline{query}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['blog']=final


def Analyzer(State:State):
    blog = State['blog']
    prompt = f"Rate this blog{blog} between range of 1-10"
    model = model.with_structured_output(Rate)
    result = model.invoke(prompt)
    State['rate']=result['rating']


def Optimization(State:State):
    blog = State['blog']
    prompt = f"refine the quality of this blog{blog}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['blog']=final
    iteration = State['iteration']
    State['iteration']=iteration+1


def Final(State:State):
    final = State['blog']
    prompt = f"Fina Blog is produced just say greeting message to user only no blog etc"
    result = model.invoke(prompt)
    modelfinal = result.content[0]['text']
    State['modelfinal']=modelfinal
    return {
        'modelfinal':modelfinal,
        'blog':State['blog']
    }



def condition(State:State):

    rate = State['rate']


    if State['iteration']<6:

        if rate > 8:
            return 'final'
        else:
            return 'optimization'
    else:
        return 'final'








graph = StateGraph(State)

graph.add_node('create',CreateBlog)
graph.add_node('analyze',Analyzer)
graph.add_node('optimization',Optimization)
graph.add_node('final',Final)


graph.add_edge(START,'create')
graph.add_edge('create','analyze')
graph.add_conditional_edges('analyze',condition)
graph.add_edge('optimization','analyze')

graph.add_edge('final',END)

connect = sqlite3.connect(database="Apple",check_same_thread=False)
checkpinter = SqliteSaver(connect)

workflow = graph.compile(checkpinter=checkpinter)
initial_state={'query':'write a blog on melboune with outline title abstraction introduction body futureoutlook concclusion references '}
config = {'configurable':{'thread_id':1}}
final = workflow.invoke(initial_state, config=config)
workflow.get_state(config)
list(workflow.get_state_history())
print(final)








