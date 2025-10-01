import NavBar from "./Components/NavBar";
import ChatPage from "./Pages/ChatPages";
import LandingPage from "./Pages/LandingPage";
import { Routes, Route } from "react-router-dom";

export default function App() {
    return (
        <div className="min-h-screen bg-[#1A1B1B] text-white flex flex-col">
            <NavBar />
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/chat" element={<ChatPage />} />
            </Routes>
        </div>
    )
}