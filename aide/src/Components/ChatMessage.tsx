export default function ChatMessage({role,text}:{role, text}){
    const isUser= role === "user";
    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2 `}>
            <div className={`max-w-ws px-4 py-2 rounded-lg ${isUser ? "bg-[#423f3b] text-white" : "bg-gray-200 text-black"}`}>
                {text}
            </div>
        </div>
    )
}