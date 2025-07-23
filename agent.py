from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
load_dotenv()

llm= ChatGoogleGenerativeAI(model='gemini-1.5-flash')

# question=input("Enter your question : ")
# reply=llm.invoke([HumanMessage(content=question)])

search_tool= TavilySearch()
tools= [
    Tool(
        name="Tavily_search",
        func=search_tool.invoke,
        description="Search the web using Tavily for up-to-date information"
    )
]
# search_result= search_tool.invoke("WHen is the next avengers movie")

agent= initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

question=input("Ask a question: ")
response= agent.invoke(question)

print("Answer: \n", response)