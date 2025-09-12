import NavBar from "./Components/NavBar";
import ChatPage from "./Pages/ChatPages";

export default function App() {
    return (
        <div className="min-h-screen bg-[#1A1B1B] text-white flex flex-col">
            <NavBar />
            <ChatPage />
        </div>
    )
}