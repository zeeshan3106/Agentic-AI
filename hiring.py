from langgraph.graph import StateGraph, START,END
from typing import TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from pymongo import MongoClient
from langchain_mogdodb import MongoDBAtlasVectorSearch
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import requests
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain_community.document_loaders import PYPDFLoader
from pydantic import BaseModel, Field
from send import EmailSend

load_dotenv()
model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite')
embedding = GoogleGenerativeAIEmbeddings(model = "")
API = ""
client = MongoClient(API)
app = FastAPI()

class State(TypedDict):
    query:str
    jobtitle:str
    job_location:str
    job_description:str
    linkedin:str
    seek:str
    indeed:str
    rate:str
    selected_cvs:list
    hremail:list
    emailstatus:str
    selected_candidates:list
    resource_list:list
    final:str


class Job(TypedDict):
    jobtitle:str
    job_location:str
    job_description:str

class CVRating(BaseModel):
    name:str
    email:str
    city:str
    rate:str
class Rating(TypedDict):
    rate:Literal[1,2,3,4,5,6,7,8,9,10]


class InterviewTime(TypedDict):
    timing:list

class Selected_Candidate(TypedDict):
    email:str
    laptop_id:str
    desk_id:str
    car_id:str




def Description(State:State):
    query = State['query']
    database = client['Hiring']
    collection = database['Description']
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'
    )
    retriever = db.as_retriever(
        search_kwargs={
            'k':20
        }
    )
    data  = retriever.invoke(query)

    prompt = F" Create a job description based on this query{query} from our dataset for this specific job foield{data} exactly in previoious formats"
    model = model.with_structured_output(Job)
    result = model.invoke(prompt)
    
    State['jobtitle']=result['jobtitle']
    State['job_location']=result['job_location']
    State['job_description']=result['job_description']
    return {
        'jobtitle':State['jobtitle'],
        'job_location': State['job_location'],
        'job_description':State['job_description']
    }

def JobsPlatforms(State:State):
    Jobs_description = State['job_description']
    job_title = State['job_location']
    job_location = State['job_location']

    linkedin_API = ""
    payload = {
        'Jobs_description':Jobs_description,
        'job_location':job_location,
        'job_title':job_title


    }
    res = requests.post(API , payload)
    Indeed_API = ""
    payload = {
        'Jobs_description':Jobs_description,
        'job_location':job_location,
        'job_title':job_title


    }
    res = requests.post(API , payload)
    Seek_API = ""
    payload = {
        'Jobs_description':Jobs_description,
        'job_location':job_location,
        'job_title':job_title


    }
    res = requests.post(API , payload)


def CV(State:State):
    description  = State['job_description']
    CVlist = []
    Cvs = [doc1-path, doc2-path,doc3-path, doc4-path,doc4-path,doc4-path,doc4-path,doc4-path,doc4-path,doc4-path ]
    for i in CVs:
        loader = PYPDFLoader(i)
        result = loader.load()
        final = result[0].page_content
        prompt  = f" if this CV{final} data vs job descrtiption{description} and make strict rate between 1-10 rage in terms of semantics and matching  "
        result = model.invoke(Rating)
        State['rate']=result['rate']
        if State['rate']>9:
            prompt = f" from this CV kindy exract name, email, contact and city"
            model = model.with_structured_output(CVRating)
            result = model.invoke(prompt)
            selected_cv = {
                'name':result['name'],
                'email':result['email'],
                'city':result['city'],
                'rate':result['rate']
            }
            CVlist.append(selected_cv)
            State['selected_cvs']=CVlist
        else:
            return 'not-matched'


def InterviewSchedule(State:State):
    database = client['Hiring']
    collection = database['Office_Shedules']
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'

    )
    retriever = db.as_retriever(
        search_kwargs={
            'k':30
        }
    )
    final = retriever.invoke("Previous interviews hiring schedule for AI Engineers")
    prompt = f"This is the previous data regarding interview times for this field i want you to give me exact perfect times for 10 individuals data also demonstrate the the free time of HR as well "
    model = model.with_structured_output(InterviewTime)
    result = model.invoke(prompt)
    timing = result['timing']
    for i in timing:
        API = "email-api"
        res = requests.post(APi,i)
    selected_cvs = State['selected_cvs']


    for i in selected_cvs:
        name = i['name']
        email = i['email']
        city = i['city']

        EmailSend(email,name, city, times)
        State['emailstatus']="semt"



def Selected(State:State):
    API = ""
    res = requests.get(API)
    emailsdatabase = client['Hiring']
    collection = emailsdatabase['emails']
    db = MongoDBAtlasVectorSearch(
        embedding = embedding,
        collection = collection,
        index_name = 'vector_index'

    )
    retriever = db.as_retriever(
        search_kwargs = {
            'k':30
        }
    )
    emailreesult = retriever.invoke("Email")

    resources_db = client['Hiring']
    collection = resources_db['Technical_Team_Resources']
    retriever = db.as_retriever(
        search_kwargs = {
            'k':100
        }
    )
    resultres = retriever.invoke("laptop unoccupied, desk unoccupied, car unoccupied ")

    resource_list = []




    for i in res:
        data = i
        prompt = f"{i}This is the individual that got selected for job kindly from our database{emailreesult} get the company emails type and with the name {i}  of the individual create company email and from this database{resultres} get the avaiabe laptop_id, desk_id and car_id each resource must not have to be this these are prohibited{resource_list} "
        model = model.with_structured_output(Selected_Candidate)
        result = model.invoke(prompt)
        resource_list.append(result)
        State['resource_list'].append(result)
        email = i['email']
        name = i['name']
        city:i['city']
        company_email = result['email']
        desk_id = result['desk_id']
        laptop_id = result['laptop_id'] 
        car_id = result['car_id'] 

        EmailSendSelected(email, name, city, company_email, desk_id, laptop_id, car_id)
    resource_list = State['resource_list']
    prompt = f"Emails to the selcted Candidates{res} {resource_list} in the company sent successfully create greeting message and list the names,emails and id's in table "
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['final']=final

    return State['final']



graph = StateGraph()
graph.add_node('desc',Description)
graph.add_node('platform', JobsPlatforms)
graph.add_node('cv',CV)
graph.add_node('interview', InterviewSchedule)
graph.add_node('selected', Selected)
graph.add_edge(START, 'desc')
graph.add_edge('desc','platform')
graph.add_edge('platform','cv')
graph.add_edge('cv','interview')
graph.add_edge('interview','selected')
graph.add_edge('selected',END)

connect = sqlite3.connect(database="ABC", check_same_thread=False)
checkpointer = SqliteSaver(connect)
workflow = graph.compile(checkpointer = checkpointer)
config = {'configurable':{'thread_id':1}}

@app
def Query(query:str = Body(...)):
    # 'a job regarding AI ML Engineer havong 2 years on experience'
    initial_state = {'query':query}
    final = workflow.invoke(initial_state, config = config)
    return JSONResponse(
        status_code = 200,
        content = final
    )










    


    


    





        












