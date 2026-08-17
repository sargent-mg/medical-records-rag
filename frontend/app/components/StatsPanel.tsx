"use client";

import { useEffect, useState } from "react";
import { Activity, Clock, MessageSquare, ThumbsUp } from "lucide-react";

interface Stats {
  total_queries: number;
  avg_latency_ms: number;
  total_feedback: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StatsPanel() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/stats`)
      .then((r) => r.json())
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const cards = stats
    ? [
        {
          label: "Total Queries",
          value: stats.total_queries,
          icon: MessageSquare,
          color: "#3b82f6",
        },
        {
          label: "Avg Latency",
          value: `${(stats.avg_latency_ms / 1000).toFixed(2)}s`,
          icon: Clock,
          color: "#8b5cf6",
        },
        {
          label: "Feedback Given",
          value: stats.total_feedback,
          icon: ThumbsUp,
          color: "#22c55e",
        },
      ]
    : [];

  return (
    <div
      style={{
        flex: 1,
        padding: "32px",
        overflowY: "auto",
      }}
    >
      <div style={{ marginBottom: "24px" }}>
        <h1
          style={{
            fontSize: "18px",
            fontWeight: 700,
            color: "var(--foreground)",
          }}
        >
          System Statistics
        </h1>
        <p style={{ fontSize: "13px", color: "var(--muted)", marginTop: "4px" }}>
          Real-time metrics from the RAG pipeline
        </p>
      </div>

      {loading ? (
        <div style={{ color: "var(--muted)", fontSize: "14px" }}>
          Loading stats...
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "16px",
            maxWidth: "700px",
          }}
        >
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.label}
                style={{
                  background: "var(--card-bg)",
                  border: "1px solid var(--border)",
                  borderRadius: "12px",
                  padding: "20px",
                  display: "flex",
                  flexDirection: "column",
                  gap: "12px",
                }}
              >
                <div
                  style={{
                    width: "36px",
                    height: "36px",
                    borderRadius: "8px",
                    background: `${card.color}18`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <Icon size={18} color={card.color} />
                </div>
                <div>
                  <div
                    style={{
                      fontSize: "24px",
                      fontWeight: 700,
                      color: "var(--foreground)",
                    }}
                  >
                    {card.value}
                  </div>
                  <div
                    style={{
                      fontSize: "12px",
                      color: "var(--muted)",
                      marginTop: "2px",
                    }}
                  >
                    {card.label}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div
        style={{
          marginTop: "32px",
          background: "var(--card-bg)",
          border: "1px solid var(--border)",
          borderRadius: "12px",
          padding: "20px",
          maxWidth: "700px",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "12px",
          }}
        >
          <Activity size={16} color="var(--primary)" />
          <span style={{ fontSize: "14px", fontWeight: 600 }}>
            Pipeline Info
          </span>
        </div>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "8px",
            fontSize: "13px",
          }}
        >
          {[
            ["Vector Store", "Qdrant"],
            ["Retrieval Mode", "Hybrid (Dense + BM25)"],
            ["Embedding Model", "text-embedding-3-small"],
            ["LLM", "GPT-4o-mini"],
            ["Total Chunks", "68,298"],
            ["Patients", "125"],
          ].map(([label, value]) => (
            <div
              key={label}
              style={{
                display: "flex",
                justifyContent: "space-between",
                padding: "6px 0",
                borderBottom: "1px solid var(--border)",
              }}
            >
              <span style={{ color: "var(--muted)" }}>{label}</span>
              <span style={{ fontWeight: 500 }}>{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}