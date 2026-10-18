from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")




class State(TypedDict):
    salary:int
    dish:str
    restaurant:str
    movie:str
    rental:str






def restaurant(State:State):
    salary = State['salary']
    dish = State['dish']
    prompt = f"Based on thsi salary give restaurants in melbourne{salary} and book the top ranked restaurant for {dish}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['restaurant']=final
    return {
        'restaurant':final
    }

def movie(State:State):
    salary = State['salary']
    dish = State['dish']
    prompt = f"Based on thsi salary give restaurants in melbourne{salary} and book the top ranked movie telecast today in melbourne cinemas "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['movie']=final
    return {
        'movie':final
    }

def carrentals(State:State):
    salary = State['salary']
    dish = State['dish']
    prompt = f"Based on thsi salary give carrentals in melbourne{salary} and book the top ranked car from top rankd rental in melbourne cinemas "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['rental']=final
    return {
        'rental':final
    }


graph = StateGraph(State)

graph.add_node('restaurant',restaurant)
graph.add_node('movie',movie)
graph.add_node('carrentals',carrentals)
graph.add_edge(START,'restaurant')
graph.add_edge(START,'movie')
graph.add_edge(START,'carrentals')
graph.add_edge('restaurant',END)
graph.add_edge('movie',END)
graph.add_edge('carrentals',END)
conncet = sqlite3.connect(database="Apple", check_same_thread=False)
checkpinter = SqliteSaver(conncet)
workflow = graph.compile(checkpinter=checkpinter)
config = {'configurable':{'thread_id':1}}
initital_state={'My salary is 150k AUD'}
final = workflow.invoke(initital_state, config=config)
workflow.get_state(config)
list(workflow.get_state_history())

print(final)






    
