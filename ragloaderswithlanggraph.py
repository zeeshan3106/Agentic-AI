from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import CSVLoader
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()
model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")

class State(TypedDict):
    query:str
    data:str
    pdf:str
    directory:str
    web:str
    llm:str
    csv:str


def Loading(State:State):
    loader = PyPDFLoader(r'C:\Users\cb\Desktop\Practice Langgraph\Australia Awards Scholarships 2027 (1).pdf')
    result = loader.lazy_load()
    print(result[0].page_content)

def CombinedData(State:State):
    loader = DirectoryLoader(
        path=r'C:\Users\cb\Desktop\Practice Langgraph\Data',
        glob='.pdf',
        loader_cls=PyPDFLoader

    )
    result = loader.lazy_load()
    final = result[0].page_content
    print(final)

def WebData(State:State):
    loader = WebBaseLoader(
        'https://www.zeeshan.com/'
    )
    result = loader.lazy_load()
    final = result[0].page_content
    State['web']=final
    return {
        'web':final
    }
def CSV(State:State):
    loader = CSVLoader(r'C:\Users\cb\Desktop\Practice Langgraph\abc.csv')
    result = loader.load()
    final = result[0].page_content
    print(final)
    State['csv']=final
    return {
        'csv':final
    }





graph = StateGraph()
graph.add_node('loading',Loading)
graph.add_node('combned',CombinedData)
graph.add_node('web',WebData)
graph.add_node('csv',CSV)
graph.add_edge(START,'loading')
graph.add_edge('loading','combined')
graph.add_edge('combined','web')
graph.add_edge('web','csv')
grah.add_edge('csv',END)

connect = sqlite3.connect(database="Abc",check_same_thread=False)
checkpointer = SqliteSaver(connect)
config={'configurable':{'thread_id':1}}

workflow = graph.compile(checkpointer=checkpointer)
initial_state={'query':'How are You?'}
final = workflow.invoke(initial_state,config = config)
print(final)
workflow.get_state(config)
print(list(workflow.get_state_history()))
