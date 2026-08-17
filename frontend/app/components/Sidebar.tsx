"use client";

import { MessageSquare, Activity, Database, Heart } from "lucide-react";

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const navItems = [
  { id: "chat", label: "Patient Query", icon: MessageSquare },
  { id: "stats", label: "System Stats", icon: Activity },
];

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <aside
      style={{
        width: "240px",
        background: "var(--sidebar-bg)",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: "24px 20px",
          borderBottom: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <Heart size={20} color="#3b82f6" />
          <div>
            <div
              style={{
                color: "#f1f5f9",
                fontWeight: 700,
                fontSize: "14px",
                letterSpacing: "0.02em",
              }}
            >
              MedRecords AI
            </div>
            <div style={{ color: "var(--sidebar-text)", fontSize: "11px" }}>
              Clinical Assistant
            </div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav style={{ padding: "12px 0", flex: 1 }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                padding: "10px 20px",
                background: isActive
                  ? "rgba(59,130,246,0.15)"
                  : "transparent",
                border: "none",
                borderLeft: isActive
                  ? "3px solid var(--sidebar-active)"
                  : "3px solid transparent",
                color: isActive ? "#f1f5f9" : "var(--sidebar-text)",
                fontSize: "13px",
                fontWeight: isActive ? 600 : 400,
                cursor: "pointer",
                textAlign: "left",
                transition: "all 0.15s",
              }}
            >
              <Icon size={16} />
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div
        style={{
          padding: "16px 20px",
          borderTop: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            color: "var(--sidebar-text)",
            fontSize: "11px",
          }}
        >
          <Database size={12} />
          Synthea Synthetic Data
        </div>
      </div>
    </aside>
  );
}