import { IoChatbubbleOutline } from "react-icons/io5";
import { TfiSearch } from "react-icons/tfi";

export default function NavBar() {
  return (
    <div>
      <div className="flex bg-[#202229] w-full p-3 pr-5 pl-5 ">
        <div className="w-1/5 transform transition duration-300 hover:scale-105">
              <IoChatbubbleOutline className="w-6 h-6"/>
        </div>
        <div className="w-3/5 text-center transform transition duration-300 hover:scale-105">
              <p>Aide</p>
        </div>
        <div className="w-1/5 flex justify-end transform transition duration-300 hover:scale-105">
              <TfiSearch className="w-6 h-6" />
        </div>
      </div>
      <hr className="border border-[#60A5FA] w-full"/>
    </div>
    
  )
}