import requests
import os
from dotenv import load_dotenv
load_dotenv()

def send_to_discord(message):
    Webhook_key=os.getenv("DISCORD_WEBHOOK")
    if not Webhook_key:
        raise ValueError("DISCORD_WEBHOOK Key not given, unavaible in the .env")
    payload={"content":message}
    response=requests.post(Webhook_key,json=payload)

    if response.status_code !=204:
        raise Exception(f"Failed to send message through discord: {response.text}")
    return "Message successfully sent through Discord"