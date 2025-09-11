import ChatMessage from "./ChatMessage";

export default function Chatwindow({messages}) {
    
    return (
        <div>
            {messages.map((m,i)=>(
                <ChatMessage key={i} role={m.role} text={m.text} />
            ))}
        </div>
    )
}