import { useNavigate } from "react-router-dom";
import { FaGithub } from "react-icons/fa";
import PixelBlast from "../Components/dotGrid";

export default function LandingPage() {
    const navigate= useNavigate()
    const handleGoToChat = () => {
        navigate('/chat')
        console.log("Routed to ChatPage");
    }
    const handleLearnMore = () => {
        window.open("https://github.com/ItsAbhinavM/Aide", "_blank");
        console.log("Learn More button clicked")
    }

    return (
        <div className="flex-1 w-full h-screen flex items-center justify-center">
            <PixelBlast
                variant="circle"
                pixelSize={6}
                color="#B19EEF"
                patternScale={3}
                patternDensity={1.2}
                pixelSizeJitter={0.5}
                enableRipples
                rippleSpeed={0.4}
                rippleThickness={0.12}
                rippleIntensityScale={1.5}
                liquid
                liquidStrength={0.12}
                liquidRadius={1.2}
                liquidWobbleSpeed={5}
                speed={0.6}
                edgeFade={0.25}
                transparent
            />
            <div className="text-center space-y-6">
                <h1 className="text-5xl font-extrabold text-white leading-tight ">Your Own Personalized Agentic AI, <br /> now easier!</h1>
                <div className="flex items-center justify-center space-x-4 pt-4">
                    <button className="px-6 py-3 rounded-full bg-white text-black font-medium shadow-md hover:bg-gray-200 transition" onClick={handleGoToChat}>Get Started</button>
                    <button className="px-6 py-3 rounded-full border border-white text-white font-medium shadow-md hover:bg-white/10 transition flex items-center gap-2" onClick={handleLearnMore}>Learn More <FaGithub className="h-5 w-5" /> </button>
                </div>
            </div>
        </div>
    )
}