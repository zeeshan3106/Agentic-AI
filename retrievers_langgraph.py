from langgraph.graph import StateGraph,START,END
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_community.retrievers import WikipediaRetriever
from langchain_mongodb import MongoDBAtlasVectorsearch
from pymongo import MongoClient

model= ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

class State(TypedDict):
    query:str
    wiki:str
    retrieved:str
    status:Literal['wiki','rag']
class Status(TypedDict):
    status:Literal['wiki','rag']

def Analyze(State:State):
    query = State['query']
    prompt = f"analyze that is this query{query} belongs to be retrieved from wokipedia or our rag data ?"
    model= model.with_structured_output(Status)
    result = model.invoke(query)
    State['status']=result['status']


def Wikipedia(State:State):
    query  = State['query']
    wiki = WikipediaRetriever(
        top_k_results=2,
        lang='eng'
    )
    result = wiki.invoke(query)
    State['wiki']=result


def database(State:State):
    embedding = GoogleGenerativeAIEmbeddings()
    query = State['query']
    client = MongoClient(API)
    database = client['Database']
    collection=database['New Collection']
    db= MongoDBAtlasVectorsearch(
        embedding = embedding,
        collection=collection,
        index_name='vector_index'


    )

    retriever = db.as_retriever(
        search_type='mmr',
        search_kwargs={'k':2}

    )
    result = retriever.invoke(query)
    State['retrieved']=result



def condition(State:State):
    status = State['status']
    if status == 'rag':
        return 'database'
    else:
        return 'wiki'




graph = StateGraph()

graph.add_node('wiki',Wikipedia)
graph.add_node('database',database)

graph.add_edge(START,condition)
graph.add_edge('wiki',END)
graph.add_edge('database',END)


workflow = graph.compile()
initial_state={'query':'When Australia was discovered and by who?'}
final = workflow.invoke(initial_state)

