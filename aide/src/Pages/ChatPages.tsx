import { useState } from "react"
import Chatwindow from "../Components/Chatwindow"
import InputBar from "../Components/InputBar"

export default function ChatPage() {
    const [messages,setMessages]=useState([]);

    const addMessage= (text)=> {
        setMessages((prev)=> [...prev,{role:"user",text}]);
    };

    return (
        <div className="flex flex-col h-screen m-20">
            {/* <SideBar /> */}
            <div className="flex-1 overflow-y-auto pb-24">
                <Chatwindow messages={messages}/>
            </div>
            <InputBar onSend={addMessage} />
        </div>
    )
}