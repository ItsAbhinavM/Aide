export default function ChatMessage({role,text}:{role, text}){
    const isUser= role === "user";
    console.log("Chat Message rendering : ",{role,text, isUser});

    if (!text) {
        console.warn("ChatMessage recieved empty text : ",{role,text});
        return null;
    }

    return (
        <div className={`flex w-full mb-2 ${isUser ? "justify-end" : "justify-start"} `}>
            <div className={`max-w-sm w-max px-4 py-2 rounded-lg break-words ${isUser ? "bg-[#423f3b] text-white-200" : "bg-black-300 text-white-100"}`}>
                {String(text)}
            </div>
        </div>
    )
}