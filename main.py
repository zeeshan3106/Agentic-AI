from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters import MultiServerMCPClient
from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
import asyncio
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')


class State(TypedDict):

    message:str
    response:str

graph = StateGraph(State)


client = MultiServerMCPClient(
   {
        "finance": {
            "transport": "stdio",
            "command": "npx",
            "args": [
                "-y",
                "@thenextgennexus/finance-mcp-server@1.0.1"
            ],
            "env": {
                "APIFY_TOKEN": os.getenv("APIFY_TOKEN")
            }
        }
    }
)


async def build_graph():
    tools = await client.get_tools()
    tools_llm = model.bind_tools(tools)
    async def chatbot(state: State):

        response = await tools_llm.ainvoke(
            state["message"]
        )

        return {
            "response": response
        }
    graph.add_node("chatbot", chatbot)


    graph.add_edge(START, "chatbot")

    graph.add_edge("chatbot", END)

    return graph.compile()


async def main():
    chatbot = await build_graph()
    res = chatbot.ainvoke(
        {
            message:"What is Love?"
        }
    )




if __name__ =='__main__':
    asyncio.run(main())

