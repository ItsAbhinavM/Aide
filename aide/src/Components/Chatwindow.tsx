import ChatMessage from "./ChatMessage";

export default function Chatwindow({messages}) {
    console.log("ChatWindow rendering with messages : ",messages)
    
    return (
        <div className="flex flex-col items-stretch w-full max-w-xl mx-auto p-4 space-y-2">
            {messages.map((m,i)=>(
                <ChatMessage key={i} role={m.role} text={m.text} />
            ))}
        </div>
    )
}