import { useRef, useState } from "react";
import { BiSolidSend } from "react-icons/bi";

export default function InputBar({onMessageExchange}) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const textareaRef = useRef(null);
  const buttonRef = useRef(null);

  async function sendMessage(e) {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage = message;
    setLoading(true);
    setMessage("");

    try {
        
        if (onMessageExchange) {
            console.log("Calling onSend with:", userMessage);
            onMessageExchange(userMessage);
        }

        
        setMessage("");

        const result = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify({ question: userMessage }),
        });

        console.log("Sending text to backend:", userMessage);
        
        if (!result.ok) {
            throw new Error(`HTTP error! status: ${result.status}`);
        }
        
        const data = await result.json();
        console.log("Backend replied:", data.response);

        if (onMessageExchange && data.response) {
            console.log("Calling onReply with:", data.response);
            onMessageExchange(data.response);
        }

    } catch (err) {
        console.error("Error occurred while sending the message:", err);
        if (onMessageExchange) {
          onMessageExchange(`Error: ${err.message}`);
        }
    } finally {
        setLoading(false);
    }
  }

  const handleInput = (e) => {
    const textarea = textareaRef.current;
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + "px";
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (buttonRef.current) {
        buttonRef.current.click();
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const prompt=textareaRef.current.value.trim()
    if (prompt){
      onMessageExchange(prompt);
        console.log("Submit clicked with text:", textareaRef.current.value);
        textareaRef.current.value="";
        textareaRef.current.style.height="auto";
    }
  };

  return (
    <form
      onSubmit={sendMessage}
      className="fixed bottom-0 left-0 w-full p-4 z-10 bg-transparent transform transition duration-300 hover:scale-105 "
    >
      <div className="mx-auto w-full max-w-2xl bg-neutral-800/70 backdrop-blur-md rounded-2xl flex items-end px-4 py-3 shadow-xl">
        <textarea
          ref={textareaRef}
          rows={1}
          maxLength={4000}
          placeholder="Ask something..."
          className="transition-[height] duration-600 ease-in-out flex-1 bg-transparent text-white pt-2 placeholder-white/50 resize-none outline-none border-none min-h-[40px] max-h-[160px] px-0 py-0 mr-3"
          style={{ overflowY: "auto" }}
          value={message}
          onInput={handleInput}
          onKeyDown={handleKeyDown}
          onChange={(e)=> setMessage(e.target.value)}
        />
        <button
          ref={buttonRef}
          type="submit"
          // onClick={sendMessage}
          className="flex items-center justify-center h-10 w-10 rounded-xl bg-transparent hover:bg-blue-600/20 transition-colors duration-200 text-blue-400"
        >
          <BiSolidSend className="w-6 h-6" />
        </button>
      </div>
    </form>
  );
}
