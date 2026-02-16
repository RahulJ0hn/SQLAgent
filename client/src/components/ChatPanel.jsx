import { useState, useRef, useEffect } from "react";
import { Send, Loader2, AlertTriangle, Database } from "lucide-react";
import { sendQuery } from "../services/api";
import ThinkingState from "./ThinkingState";
import SQLDisplay from "./SQLDisplay";
import ResultTable from "./ResultTable";
import ChartRenderer from "./ChartRenderer";

export default function ChatPanel({ messages, setMessages, activeChatId, onFirstMessage }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput("");

    const userMsg = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      timestamp: new Date(),
    };

    // Always send to the backend — LLM handles intent classification
    if (!activeChatId) {
      onFirstMessage(userMsg);
    } else {
      setMessages((prev) => [...prev, userMsg]);
    }
    setLoading(true);

    try {
      const response = await sendQuery(question);
      const assistantMsg = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.final_answer,
        response: response.type === "data" ? response : null,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const detail = err?.response?.data?.error || err?.response?.data?.detail || err?.message || "Something went wrong";
      const assistantMsg = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: `Sorry, I couldn't process that. ${detail}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } finally {
      setLoading(false);
    }
  };

  // Check if response has actual SQL data
  const hasSQLData = (response) => {
    return response && response.type === "data" && response.sql && response.result && response.result.length > 0;
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Database className="w-16 h-16 text-blue-400/50 mb-4" />
            <h2 className="text-2xl font-semibold text-gray-300">
              What would you like to know?
            </h2>
            <p className="text-gray-500 mt-2 max-w-md">
              Ask questions about your data in plain English. I'll generate SQL, execute it safely, and visualize the results.
            </p>
            <div className="mt-6 grid grid-cols-2 gap-2 max-w-lg">
              {[
                "Top 10 customers by revenue",
                "Monthly revenue trends",
                "Active subscriptions per plan",
                "Open support tickets by priority",
              ].map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  className="px-4 py-3 rounded-xl bg-gray-800/50 border border-gray-700/50 text-sm text-gray-400 hover:text-white hover:bg-gray-800 hover:border-gray-600 transition-all text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className="space-y-3">
            {msg.role === "user" ? (
              <div className="flex justify-end">
                <div className="max-w-2xl px-4 py-2.5 rounded-2xl bg-blue-600 text-white">
                  {msg.content}
                </div>
              </div>
            ) : (
              <div className="space-y-4 max-w-4xl">
                {/* Only show reasoning/SQL/charts for actual data queries */}
                {hasSQLData(msg.response) && (
                  <>
                    {msg.response.reasoning?.length > 0 && (
                      <ThinkingState steps={msg.response.reasoning} />
                    )}

                    {msg.response.sql && <SQLDisplay sql={msg.response.sql} />}

                    <ChartRenderer
                      chartType={msg.response.chart_type}
                      data={msg.response.result}
                      columns={msg.response.columns}
                    />

                    <ResultTable
                      columns={msg.response.columns}
                      data={msg.response.result}
                      rowCount={msg.response.row_count}
                    />
                  </>
                )}

                {/* Text answer */}
                <div className="px-4 py-3 rounded-2xl bg-gray-800 text-gray-200 whitespace-pre-line">
                  {msg.response?.attempts > 1 && (
                    <div className="flex items-center gap-1.5 text-xs text-amber-400 mb-2">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      Self-healed after {msg.response.attempts} attempts
                    </div>
                  )}
                  {msg.content}
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-gray-400 text-sm p-4">
            <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
            <span>Processing your question...</span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-800 p-4">
        <form onSubmit={handleSubmit} className="flex gap-3 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your data..."
            className="flex-1 px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-4 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
