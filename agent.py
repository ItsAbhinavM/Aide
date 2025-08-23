from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_tavily import TavilySearch
from langchain.agents import initialize_agent, AgentType
from Components.discord import send_to_discord
from Components.youtube import youtube_loader
from langchain_core.tools import Tool, tool
load_dotenv()

system_prompt_template = """
You are an orchestrator Agent and a reliable personal assistant.
Your primary role is to coordinate tools and provide clear, structured and helpful response.

Available capabilities:
1. **Write detailed notes**  
   - Convert raw text or transcripts into well-organized notes.  
   - Always include main topics, subtopics, key points, and a short summary.  
2. **YouTube Transcript + Inference**  
   - If the user provides a valid YouTube link, fetch the transcript.  
   - Then create structured notes or a clear summary of the video’s content.  

3. **Discord Messaging**  
   - If the user explicitly asks you to send a message to Discord, use the Discord tool.  
   - Confirm with the user before sending sensitive content.
4. **Object detection**
    - If the user explicity asks for whats there infront of him, use the Object detector tool.
    - Describe the detected objects clearly, including positions or counts only if relevant.

General rules:
- Always decide the best tool to use based on the user's request.
- If multiple tools are needed, (e.g., YouTube transcript → detailed notes), orchestrate them step by step. 
- If the request is outside the capabilities, politely explain your limitations.
- Ensure responses are professional, consise and actionable.
"""

system_prompt= ChatPromptTemplate.from_messages([
    ("system",system_prompt_template),
    ("human","{input}")
])

search_tool= TavilySearch(max_results=1)

@tool
def send_to_discord_tool(message: str)-> str:
    """Send a message through Discord."""
    return send_to_discord(message)

@tool
def get_youtube_transcript_tool(link: str)-> str:
    """
    Gets the transcript/notes from a YouTube video. 
    Provide a valid YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID or https://youtu.be/VIDEO_ID).
    Returns detailed transcript with timestamps.
    """
    return youtube_loader(link)

@tool
def create_detailed_notes_tool(transcript: str)->str:
    """
    Creates detailed and structure notes from a YouTube video which has captions turned available.
    """
    notes_prompt=f"""
        Please create detailed, well-structured notes from the following YouTube video transcript.
        Organize the content into clear sections with:
        - Main topics and subtopics
        - Key points and important  information
        - Actionable insights if any
        - Summay at the end
        Transcript:
        {transcript}

        Please format the notes in a clear, readable structure with headings and bullet points.
    """
    response=llm.invoke([HumanMessage(content=notes_prompt)])
    return response.content


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
    ),
    Tool(
        name="Get_youtube_transcript",
        func=get_youtube_transcript_tool,
        description="Gets notes of youtube video. Use this when user provides a YouTube link."
    ),
    Tool(
        name="Create_detailed_notes",
        func=create_detailed_notes_tool,
        description="Creates structured, detailed notes from a transcript. Use this after getting a YouTube transcript to format it into organized notes."
    )
]
# search_result= search_tool.invoke("WHen is the next avengers movie")

llm= ChatGoogleGenerativeAI(model='gemini-1.5-flash',system_instruction=system_prompt_template)
orchestrator_chain= system_prompt | llm | StrOutputParser()

agent= initialize_agent(
    tools=tools,
    llm=orchestrator_chain,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # does a reasoning before description
    verbose=True,
    handle_parsing_errors=True
)

if __name__=="__main__":
    try:
        question=input("Ask a question: ")
        response= agent.invoke(question)

        print("Answer: \n", response)
    except Exception as e:
        print(f"Error: {e}")
        print("Please try again with a different question or check your prompt.")