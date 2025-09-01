import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_tavily import TavilySearch
from langchain.agents import initialize_agent, AgentType
from Components.discord import send_to_discord
from Components.youtube import youtube_loader
from Components.Object_detection import object_detection
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
    - If the user asks what's in front of them, what they can see, or asks about objects in view, use the Object detector tool.
    - Describe the detected objects clearly, including confidence levels if relevant.
    - The tool captures video for a few seconds to detect objects.

General rules:
- Always decide the best tool to use based on the user's request.
- If multiple tools are needed, (e.g., YouTube transcript → detailed notes), orchestrate them step by step. 
- If the request is outside the capabilities, politely explain your limitations.
- Ensure responses are professional, consise and actionable.
- If you are unsure about the user's prompt you can ask again to make it clear, or say you are unclear rather than halucinating.
"""

system_prompt= ChatPromptTemplate.from_messages([
    ("system",system_prompt_template),
    ("user","{input}")
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

@tool
def detect_objects_tool(_: str="")->str:
    """
    Detects objects in front of the user's webcam using YOLO object detection.
    Use this when the user asks about what's in front of them, what they can see, or wants to know about objects in their environment.
    Since you do not have a camera or webcam, the user has so you can use this tool for getting the object details, so that you get an idea of what is there in front of you. The object detection function inside this tool will give you the list.
    The tool will capture video for a few seconds and return detected objects.
    """
    try:
        print("Starting Object detection")
        detections=object_detection(duration=2)
        # print("GOING TO SLEEP FOR 3 SECONDS")
        # time.sleep(3)
        if "error" in detections:
            return f"Error: {detections['error']}"
        if not detections:
            return "No objects were found"
        detected_objects=[]
        confidence_threshold=0.75
        for track_id,history in detections.items():
            for label,conf in history:
                if conf>confidence_threshold:
                    detected_objects.append(f"{label}({conf*100:.1f}%)")

        detection_prompt=f"""
            I detected the following objects from the user's webcam:
            {detected_objects}
            Please provide a natural, conversational summary of what's in front of what's infront of the user. Be specific about the objects but keep the responses consises and friendly.
        """

        response=llm.invoke([HumanMessage(content=detection_prompt)])
        return response.content

    except Exception as e:
        return f"Error during object detection {str(e)}"

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
    ),
    Tool(
        name='Detect_objects_through_webcam',
        func=detect_objects_tool,
        description="Detect objects in front of user through webcam. Use when user asks 'what's in front of me', 'what can you see', or similar questions"
    )
]
# search_result= search_tool.invoke("WHen is the next avengers movie")

llm= ChatGoogleGenerativeAI(model='gemini-1.5-flash',system_instruction=system_prompt_template)
orchestrator_chain= system_prompt | llm | StrOutputParser()

agent= initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # does a reasoning before description
    verbose=True,
    max_iterations=5,
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