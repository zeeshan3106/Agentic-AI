from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

class State(TypedDict):
    title:str
    outline:str
    blog:str
    status:Literal['approved','optimization']
    aproved:str
    optimization:str
    iteration:int


class StatusScema(BaseModel):
    score:Literal['approved','optimization']




def outline_node(State:State):
    title=State['title']
    prompt =f"Create chepap little unstructured old style with wrong grammer outline for this title{title}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['outline']=final
    outline = final
    return {'outline':outline}

def blog_node(State:State):
    outline=State['outline']
    
    prompt =f"Create the cheap un structured blog with this with wrong grammer ooutline{outline}"
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['blog']=final
    return {'blog':final}


def analyze_node(State:State):
    blog = State['blog']
    prompt = f"""
 You are a STRICT professional blog quality evaluator.

Evaluate this blog on:
- Grammar
- Readability
- SEO
- Structure
- Engagement
- Clarity
- Accuracy
- Originality
- Usefulness
- Modern content quality

Be critical. Do NOT approve a blog just because it is readable.

Approve ONLY if the blog is genuinely publication-ready and would deserve
at least 9/10 overall quality.

If it is not at least 8/10, return "optimization".

Return ONLY:
"approved"
or
"optimization"

Blog:
{blog}
    """
    models = model.with_structured_output(StatusScema)
    result = models.invoke(prompt)
    final = result.score
    iteration = State['iteration']
    if iteration >= 5:
        State['status']="approved"
    else:
        State['status']=result.score



    return {'status': State['status']}


def optimization_node(State:State):
    blog = State['blog']
    prompt = f"""
    You are an expert blog editor and content optimizer.

    Improve the following blog while preserving its original meaning,
    main ideas, and intended audience.

    Improve these areas:
    - Grammar and spelling
    - Readability and sentence flow
    - SEO optimization
    - Structure and organization
    - Engagement
    - Clarity
    - Overall content quality

    Also apply modern content-writing practices where appropriate:
    - Create a stronger and more engaging introduction
    - Use clear headings and subheadings
    - Improve paragraph structure and transitions
    - Remove unnecessary repetition and filler
    - Make the writing natural and human-like
    - Add relevant examples where they improve understanding
    - Use concise, easy-to-scan paragraphs
    - Improve the title if necessary
    - Naturally incorporate relevant keywords without keyword stuffing
    - Add a strong conclusion
    - Make the content more useful and actionable
    - Improve the overall reader experience

    Do NOT change the core meaning of the blog.
    Do NOT invent facts, statistics, sources, or claims.
    Do NOT add irrelevant information.

    Return only the improved blog.

    Original blog:
    {blog}
    """
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['blog']=final
    iteration = State['iteration']
    State[iteration]=iteration+1
    print(iteration+1)

    return {'blog':final,"iteration": iteration + 1}

def Approved(State:State):
    prompt = f"""
    Ypur blog is approved and its on top quality
    give user the congratulations and greeting words modern style
    """
    result = model.invoke(prompt)
    final = result.content[0]['text']
    State['aproved']=final
    return State


def condition(State:State):
    status = State['status']
    if status == 'approved':
        return "approved_node"
    if status == 'optimization':
        return 'optimization_node'





graph = StateGraph(State)
graph.add_node('outline_node',outline_node)
graph.add_node('blog_node',blog_node)
graph.add_node('optimization_node',optimization_node)
graph.add_node('approved_node',Approved)
graph.add_node('analyze_node',analyze_node)

graph.add_edge(START,'outline_node')
graph.add_edge('outline_node','blog_node')
graph.add_edge('blog_node','analyze_node')
graph.add_conditional_edges('analyze_node',condition)
graph.add_edge('optimization_node','analyze_node')
graph.add_edge('approved_node',END)

workflow = graph.compile()
initial_state = {'title':'Pakistan', "iteration":0}
a = workflow.invoke(initial_state)
print(a)


