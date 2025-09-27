export default function ChatMessage({role,text}:{role, text}){
    const isUser= role === "user";
    console.log("Chat Message rendering : ",{role,text, isUser});

    if (!text) {
        console.warn("ChatMessage recieved empty text : ",{role,text});
        return null;
    }

    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
            <div className={`max-w-xs w-max px-4 py-2 rounded-lg ${isUser ? "bg-[#423f3b] text-white" : "bg-gray-200 text-black"}`}>
                {String(text)}
            </div>
        </div>
    )
}