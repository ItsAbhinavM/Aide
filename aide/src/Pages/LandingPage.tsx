import { useNavigate } from "react-router-dom";

export default function LandingPage() {
    const navigate= useNavigate()
    const handleGoToChat = () => {
        navigate('/chat')
        console.log("Routed to ChatPage");
    }

    return (
        <div className="flex-1 w-full h-screen flex items-center justify-center">
            <div className="text-center space-y-6">
                <h1 className="text-5xl font-extrabold text-white leading-tight animate-pulse">Personalized Orchestration,<br /> Now Easier!</h1>

                <div className="flex items-center justify-center space-x-4 pt-4">
                    <button className="px-6 py-3 rounded-full bg-white text-black font-medium shadow-md hover:bg-gray-200 transition" onClick={handleGoToChat}>Get Started</button>
                    <button className="px-6 py-3 rounded-full bg-white text-black font-medium shadow-md hover:bg-gray-200 transition">Learn More</button>
                </div>
            </div>
        </div>
    )
}