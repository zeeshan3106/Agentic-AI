from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter,Language
from langchain_experimental import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')
class State(TypedDict):
    query:str
    character:str


def Spliter(State:State):
    data = """
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf

    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    """
    spliter = CharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=0,
        seperator=''
    )
    result = spliter.split_text()



def Recusrive(State:State):
    data = """
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf

    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    """
    Spliter = RecursiveCharacterTextSplitter(
        chunk_size=15,
        chunk_overlap=0,
        seperator='-'
    )
    result = Spliter.split_text(data)
    print(result)
def RecusriveLanguage(State:State):
    data = """
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf

    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    """
    Spliter = RecursiveCharacterTextSplitter.from_language(
        Language=Language.PYTHON,
        chunk_size=15,
        chunk_overlap=0,
        seperator='-'

    )
    result = Spliter.split_text(data)
    print(result)

def Semantics(State:State):
    data = """
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf

    thhthereehrjehjsfsjfdhfdghrht kfdhfdfhdhfjdh dfhdhfdhfjdhjf dhfjdhfdjfdjhfdjhfdjhfd dhfjhdjfhdjhf
    """
    Spliter = SemanticChunker(
        GoogleGenerativeAIEmbeddings,
        break_threshold_type="standard_deviation",
        break_threshold_amount=1

    )
    result = Spliter.split_text(data)
    print(result)


graph=StateGraph()

graph.add_node('spliter',Spliter)
graph.add_node('recursive',Recusrive)

graph.add_edge(START, 'spliter')
graph.add_edge('spliter','recursive')
graph.add_edge('recursive',END)

connect = sqlite3.connect(database="ABC",check_same_thread=False)
checkpointer = SqliteSaver()
config = {'configurable':{'thread_id':1}}
workflow = graph.compile(checkpointer=checkpointer)
initial_state={'query':'who are you'}
final = workflow.invoke(initial_state, config = config)

workflow.get_state()
print(list[workflow.get_state_history()])
