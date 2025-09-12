import { useState } from "react"
import Chatwindow from "../Components/Chatwindow"
import InputBar from "../Components/InputBar"

export default function ChatPage() {
    const [messages,setMessages]=useState([]);

    const addMessage= (text)=> {
        setMessages((prev)=> [...prev,{role:"user",text}]);
    };

    return (
        <div>
             { messages.length===0 ? 
                <div className="h-screen flex items-center justify-center transform transition duration-300 hover:scale-105">
                    <h1 className="text-4xl font-bold mb-10">Welcome back!</h1>
                </div> : null
            }
            <div className="flex flex-col h-screen m-20 overflow-y">
                {/* <SideBar /> */}
                <div className="">
                    <Chatwindow messages={messages}/>
                </div>
                <InputBar onSend={addMessage} />
            </div>
        </div>
    )
}