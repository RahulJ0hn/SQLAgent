import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";

export default function App() {
  // Each chat = { id, title, messages: [] }
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeChat = chats.find((c) => c.id === activeChatId);
  const activeMessages = activeChat?.messages || [];

  const handleNewChat = () => {
    setActiveChatId(null); // Go to welcome screen
  };

  const handleSelectChat = (chatId) => {
    setActiveChatId(chatId);
    setSidebarOpen(false); // close sidebar on mobile after selecting
  };

  const setMessages = (updater) => {
    setChats((prev) => {
      // Find the active chat (could be the most recently created one)
      const targetId = activeChatId || (prev.length > 0 ? prev[0].id : null);
      if (!targetId) return prev;
      return prev.map((c) =>
        c.id === targetId
          ? { ...c, messages: typeof updater === "function" ? updater(c.messages) : updater }
          : c
      );
    });
  };

  const handleFirstMessage = (userMsg, assistantMsg) => {
    // Create a new chat session on the first message
    const msgs = assistantMsg ? [userMsg, assistantMsg] : [userMsg];
    const newChat = {
      id: crypto.randomUUID(),
      title: userMsg.content.length > 40 ? userMsg.content.slice(0, 40) + "..." : userMsg.content,
      messages: msgs,
    };
    setChats((prev) => [newChat, ...prev]);
    setActiveChatId(newChat.id);
    return newChat.id;
  };

  return (
    <div className="flex h-screen relative">
      {/* Overlay when sidebar is open on mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <div className="flex-1 flex flex-col min-w-0">
        <ChatPanel
          messages={activeMessages}
          setMessages={setMessages}
          activeChatId={activeChatId}
          onFirstMessage={handleFirstMessage}
          onToggleSidebar={() => setSidebarOpen((v) => !v)}
        />
      </div>
    </div>
  );
}
