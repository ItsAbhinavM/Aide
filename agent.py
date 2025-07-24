from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain.agents import initialize_agent, AgentType
from discord import send_to_discord
from langchain_core.tools import Tool, tool
load_dotenv()

llm= ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# question=input("Enter your question : ")
# reply=llm.invoke([HumanMessage(content=question)])

search_tool= TavilySearch(max_results=1)

@tool
def send_to_discord_tool(message: str)-> str:
    """Send a message through Discord."""
    return send_to_discord(message)

tools= [
    Tool(
        name="Tavily_search",
        func=search_tool.invoke,
        description="Search the web using Tavily for up-to-date information"
    ),
    Tool(
        name="Send_to_discord",
        func=send_to_discord_tool,
        description="Send messages through discord",
        return_direct=True
    )
]
# search_result= search_tool.invoke("WHen is the next avengers movie")

agent= initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # does a reasoning before description
    verbose=True
)

question=input("Ask a question: ")
response= agent.invoke(question)

print("Answer: \n", response)