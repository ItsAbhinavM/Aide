export default function NavBar() {
  return (
    <div className="w-full flex justify-center mt-6">
      <div className="flex items-center justify-between w-[90%] max-w-4xl px-6 py-3 
                      bg-[#202229]/80 backdrop-blur-md border border-white/10
                      rounded-full shadow-lg">
        
        <div className="flex items-center space-x-2">
          <img className="h-13 w-12 object-contain" src="./src/assets/aideLogo.png" />
          <span className="text-white font-semibold text-2xl">Aide</span>
        </div>

        <div className="flex space-x-6 text-white">
          <a href="#" className="hover:text-blue-400 transition text-xl">New Chat + </a>
        </div>
      </div>
    </div>
  );
}
