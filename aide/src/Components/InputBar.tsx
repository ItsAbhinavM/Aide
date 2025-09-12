import { useRef } from "react";
import { BiSolidSend } from "react-icons/bi";

export default function InputBar({onSend}) {
  const textareaRef = useRef(null);
  const buttonRef = useRef(null);

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
        onSend(prompt);
        console.log("Submit clicked with text:", textareaRef.current.value);
        textareaRef.current.value="";
        textareaRef.current.style.height="auto";
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
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
          onInput={handleInput}
          onKeyDown={handleKeyDown}
        />
        <button
          ref={buttonRef}
          type="submit"
          className="flex items-center justify-center h-10 w-10 rounded-xl bg-transparent hover:bg-blue-600/20 transition-colors duration-200 text-blue-400"
        >
          <BiSolidSend className="w-6 h-6" />
        </button>
      </div>
    </form>
  );
}
