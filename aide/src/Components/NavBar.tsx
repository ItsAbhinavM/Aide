import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoHome } from "react-icons/go";

export default function NavBar() {
  const [cleared,setCleared] = useState(false);
  const [isChatEmpty,setIsChatEmtpy] = useState(() => localStorage.length === 0);

  const clearChatHistory = (e:any) => {
      e.preventDefault();
      localStorage.clear()
      setIsChatEmtpy(true);
      setCleared(!cleared)
      window.location.reload();
      console.log("Chat history cleared");
  }

  useEffect(() => {
    const sync = () => setIsChatEmtpy(localStorage.length === 0);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener("storage", sync);
    };
  }, []);

  const navigate = useNavigate();
  const goBackHome = () => {
    navigate("/");
    console.log("Navigated back to home page");
  }

  return (
    <div className="w-full flex justify-center mt-6">
      <div className={`flex items-center justify-between w-[90%] max-w-4xl px-6 py-3 
                      bg-[#202229]/80 backdrop-blur-md border border-white/10
                      rounded-full shadow-lg ${isChatEmpty ? "justify-between" : "justify-center"}`}>
        <div className={`${isChatEmpty ? "flex-1 flex justify-center items-center space-x-2" : "flex items-center space-x-2"}`} >
          <img className="h-13 w-12 object-contain" src="./src/assets/aideLogo.png" />
          <span className="text-white font-semibold text-2xl">Aide</span>
        </div>
          <div className="flex space-x-6 text-white">
            { !isChatEmpty &&  (
              <button className="hover:text-blue-400 transition text-xl" onClick={clearChatHistory}>New Chat + </button>
            ) }
            <button className="hover:text-blue-400 transition text-xl" onClick={goBackHome}> <GoHome /> </button>
          </div>
      </div>
    </div>
  );
}
