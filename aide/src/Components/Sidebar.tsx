export default function SideBar() {
    return (
        <div className="w-64 bg-gray-900 text-white p-4 left-0">
            <h2 className="text-xl font-bold mb-4">Conversations</h2>
            <ul >
                <li className="mb-2 cursor-pointer hover:bg-gray-800 p-2 rounded">Chat 1</li>
                <li className="mb-2 cursor-pointer hover:bg-gray-800 p-2 rounded">Chat 2</li>
            </ul>
        </div>
    )
}