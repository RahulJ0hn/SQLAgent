import { MessageSquare, Plus, Database, X } from "lucide-react";

export default function Sidebar({ chats, activeChatId, onNewChat, onSelectChat, isOpen, onClose }) {
  return (
    <div
      className={`fixed lg:static inset-y-0 left-0 z-30 w-64 bg-gray-900 border-r border-gray-800 flex flex-col h-full transform transition-transform duration-300 ease-in-out ${
        isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      }`}
    >
      {/* Header */}
      <div className="p-4 border-b border-gray-800 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-lg font-semibold">
            <Database className="w-5 h-5 text-blue-400" />
            SQL Agent
          </div>
          <p className="text-xs text-gray-500 mt-1">Enterprise Assistant</p>
        </div>
        <button
          onClick={onClose}
          className="lg:hidden p-1.5 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* New Chat */}
      <div className="p-3">
        <button
          onClick={() => { onNewChat(); onClose(); }}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-700 hover:bg-gray-800 transition-colors text-sm text-gray-300"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto px-3 space-y-1">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelectChat(chat.id)}
            className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors text-left ${
              chat.id === activeChatId
                ? "bg-gray-800 text-white"
                : "hover:bg-gray-800/50 text-gray-400"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5 shrink-0" />
            <span className="text-sm truncate">{chat.title}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
