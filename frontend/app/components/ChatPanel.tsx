"use client";

import { useState, useRef, useEffect } from "react";
import { Send, ThumbsUp, ThumbsDown, Loader2 } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  queryLogId?: string;
  sources?: string[];
  feedback?: "up" | "down";
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, session_id: sessionId }),
      });
      const data = await res.json();
      setSessionId(data.session_id);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          queryLogId: data.query_log_id,
          sources: data.sources,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error connecting to the API." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  async function submitFeedback(
    queryLogId: string,
    rating: number,
    index: number,
    type: "up" | "down"
  ) {
    await fetch(`${API_URL}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query_log_id: queryLogId, rating }),
    });
    setMessages((prev) =>
      prev.map((m, i) => (i === index ? { ...m, feedback: type } : m))
    );
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        flex: 1,
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "16px 24px",
          borderBottom: "1px solid var(--border)",
          background: "var(--card-bg)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div>
          <h1 style={{ fontSize: "16px", fontWeight: 700, color: "var(--foreground)" }}>
            Patient Records Query
          </h1>
          <p style={{ fontSize: "12px", color: "var(--muted)", marginTop: "2px" }}>
            Ask questions about patient conditions, medications, and lab results
          </p>
        </div>
        {sessionId && (
          <div
            style={{
              fontSize: "11px",
              color: "var(--muted)",
              background: "var(--background)",
              padding: "4px 10px",
              borderRadius: "20px",
              border: "1px solid var(--border)",
            }}
          >
            Session active
          </div>
        )}
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "24px",
          display: "flex",
          flexDirection: "column",
          gap: "16px",
        }}
      >
        {messages.length === 0 && (
          <div
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--muted)",
              gap: "12px",
              paddingTop: "80px",
            }}
          >
            <div style={{ fontSize: "32px" }}>🏥</div>
            <div style={{ fontSize: "15px", fontWeight: 500 }}>
              Ask about your patients
            </div>
            <div style={{ fontSize: "13px", maxWidth: "380px", textAlign: "center" }}>
              Try: &quot;Which patients have diabetes?&quot; or &quot;What medications is
              Dannielle Goldner taking?&quot;
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: msg.role === "user" ? "flex-end" : "flex-start",
              gap: "6px",
            }}
          >
            <div
              style={{
                maxWidth: "72%",
                padding: "12px 16px",
                borderRadius: msg.role === "user" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
                background: msg.role === "user" ? "var(--primary)" : "var(--card-bg)",
                color: msg.role === "user" ? "#fff" : "var(--foreground)",
                fontSize: "14px",
                lineHeight: "1.6",
                border: msg.role === "assistant" ? "1px solid var(--border)" : "none",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.content}
            </div>

            {/* Sources */}
            {msg.sources && msg.sources.length > 0 && (
              <div
                style={{
                  maxWidth: "72%",
                  fontSize: "11px",
                  color: "var(--muted)",
                  background: "#f8fafc",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  padding: "8px 12px",
                }}
              >
                <div style={{ fontWeight: 600, marginBottom: "4px" }}>
                  Retrieved sources ({msg.sources.length})
                </div>
                {msg.sources.slice(0, 3).map((src, j) => (
                  <div
                    key={j}
                    style={{
                      padding: "2px 0",
                      borderTop: j > 0 ? "1px solid var(--border)" : "none",
                      marginTop: j > 0 ? "4px" : "0",
                    }}
                  >
                    {src}
                  </div>
                ))}
              </div>
            )}

            {/* Feedback */}
            {msg.role === "assistant" && msg.queryLogId && (
              <div style={{ display: "flex", gap: "6px" }}>
                <button
                  onClick={() =>
                    submitFeedback(msg.queryLogId!, 5, i, "up")
                  }
                  style={{
                    background: msg.feedback === "up" ? "var(--success)" : "var(--card-bg)",
                    color: msg.feedback === "up" ? "#fff" : "var(--muted)",
                    border: "1px solid var(--border)",
                    borderRadius: "6px",
                    padding: "4px 8px",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                    fontSize: "12px",
                  }}
                >
                  <ThumbsUp size={12} />
                </button>
                <button
                  onClick={() =>
                    submitFeedback(msg.queryLogId!, 1, i, "down")
                  }
                  style={{
                    background: msg.feedback === "down" ? "var(--danger)" : "var(--card-bg)",
                    color: msg.feedback === "down" ? "#fff" : "var(--muted)",
                    border: "1px solid var(--border)",
                    borderRadius: "6px",
                    padding: "4px 8px",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "4px",
                    fontSize: "12px",
                  }}
                >
                  <ThumbsDown size={12} />
                </button>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--muted)" }}>
            <Loader2 size={14} style={{ animation: "spin 1s linear infinite" }} />
            <span style={{ fontSize: "13px" }}>Querying records...</span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div
        style={{
          padding: "16px 24px",
          borderTop: "1px solid var(--border)",
          background: "var(--card-bg)",
          display: "flex",
          gap: "10px",
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
          placeholder="Ask about patient records..."
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid var(--border)",
            fontSize: "14px",
            outline: "none",
            background: "var(--background)",
            color: "var(--foreground)",
          }}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          style={{
            background: "var(--primary)",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            padding: "10px 16px",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            opacity: loading || !input.trim() ? 0.5 : 1,
            display: "flex",
            alignItems: "center",
            gap: "6px",
            fontSize: "14px",
            fontWeight: 500,
          }}
        >
          <Send size={14} />
          Send
        </button>
      </div>
    </div>
  );
}