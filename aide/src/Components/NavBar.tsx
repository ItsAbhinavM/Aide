import { LuPaperclip } from "react-icons/lu";

export default function NavBar() {
  return (
    <div>
      <div className="flex bg-[#202229] w-full p-3 ">
        <div className="w-1/5">
              <LuPaperclip className="w-6 h-6"/>
        </div>
        <div className="w-3/5 text-center">
              <p>Aide</p>
        </div>
        <div className="w-1/5">
              <p>Other Icons</p>
        </div>
      </div>
      <hr className="border border-[#60A5FA] w-full"/>
    </div>
    
  )
}