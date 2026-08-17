"use client";

import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import StatsPanel from "./components/StatsPanel";

export default function Home() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main style={{ flex: 1, overflow: "hidden", display: "flex" }}>
        {activeTab === "chat" && <ChatPanel />}
        {activeTab === "stats" && <StatsPanel />}
      </main>
    </div>
  );
}