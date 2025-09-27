import { useState, useEffect } from "react"
import Chatwindow from "../Components/Chatwindow"
import InputBar from "../Components/InputBar"

export default function ChatPage() {
    const [messages, setMessages] = useState([]);

    const handleMessageExchange = (userMessage, botReply) => {
        console.log("Adding user message:", userMessage);
        console.log("Adding bot reply:", botReply);
        
        setMessages((prev) => {
            const newMessages = [
                ...prev,
                { role: "user", text: userMessage },
                { role: "assistant", text: botReply } 
            ];
            console.log("New messages state:", newMessages);
            return newMessages;
        });
    };

    // Debug the messages state
    useEffect(() => {
        console.log("Current messages in state:", messages);
    }, [messages]);

    return (
        <div>
            {messages.length === 0 ? (
                <div className="h-screen animate-pulse flex items-center justify-center transform transition duration-300 hover:scale-105">
                    <h1 className="text-5xl font-bold mb-10">Welcome back!</h1>
                </div>
            ) : null}
            <div className="flex flex-col h-screen m-20 overflow-y">
                <div className="">
                    <Chatwindow messages={messages} />
                </div>
                <InputBar onMessageExchange={handleMessageExchange} />
            </div>
        </div>
    );
}