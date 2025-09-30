export default function ChatMessage({role,text}:{role, text}){
    const isUser= role === "user";
    console.log("Chat Message rendering : ",{role,text, isUser});
    var count=0;
    if (!text) {
        console.warn("ChatMessage recieved empty text : ",{role,text});
        return null;
    }

    if (isUser&&count%2==0) {
        return (
            <div className={`flex w-full mb-2 justify-end `}>
                <div className={`max-w-sm w-max px-4 py-2 rounded-lg break-words bg-[#423f3b] text-white-200`}>
                    {String(text)}
                </div>
            </div>
        );
    } else {
        if (count%2!=0){
            count++;
        }
    }

    return (
        <div className={`flex w-full justify-start`}>
            <div className={`prose prose-invert max-w-none whitespace-pre-wrap`}>
                {String(text)}
            </div>
        </div>
    );
}