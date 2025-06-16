from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv()

llm= ChatGoogleGenerativeAI(model='gemini-1.5-flash')
question=input("Enter your question : ")
reply=llm.invoke([HumanMessage(content=question)])

print("Hello world")
print(reply.content)
