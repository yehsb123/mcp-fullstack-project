"use client";

import { useState } from "react";

const API_BASE = "http://localhost:8000/api/v1";

// --- 멘토 제공: 타입 정의 ---
interface ChatMessage {
  role: "user" | "agent";
  content: string;
  decision?: string;
  actions?: string[];
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [userId, setUserId] = useState("1");
  const [loading, setLoading] = useState(false);

  // --- 채팅 전송 (3주차) ---
  // TODO: fetch로 POST /api/v1/agent/chat 호출
  // ★ page.tsx의 handleSubmit과 동일한 fetch 패턴입니다!
  const handleSend = async () => {
    if (!input.trim()) return;

    // --- 멘토 제공: 사용자 메시지를 화면에 추가 ---
    const userMsg: ChatMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    const messageText = input;
    setInput("");
    setLoading(true);

    // TODO: 아래 2~3단계를 구현하세요
    //
    // --- 2단계: fetch로 Agent API 호출 ---
    // const res = await fetch(`${API_BASE}/agent/chat`, {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({
    //     message: messageText,
    //     user_id: Number(userId),
    //   }),
    // });
    // const data = await res.json();
    //
    // --- 3단계: Agent 응답을 화면에 추가 ---
    // const agentMsg: ChatMessage = {
    //   role: "agent",
    //   content: data.reasoning,
    //   decision: data.decision,
    //   actions: data.actions_taken,
    // };
    // setMessages((prev) => [...prev, agentMsg]);

    setLoading(false);
  };

  // --- 멘토 제공: Enter키로 전송 ---
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // --- 멘토 제공: UI (수정하지 마세요) ---
  return (
    <div style={{ maxWidth: 700, margin: "0 auto", padding: 40, height: "100vh", display: "flex", flexDirection: "column" }}>
      <h1 style={{ marginBottom: 8 }}>AccessGuard - AI 권한 심사</h1>
      <div style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
        <label style={{ fontSize: 14, color: "#666" }}>사용자 ID:</label>
        <input
          type="number"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          style={{ padding: "4px 8px", width: 80, border: "1px solid #ddd", borderRadius: 4 }}
        />
      </div>

      {/* 메시지 목록 */}
      <div style={{
        flex: 1, overflowY: "auto", border: "1px solid #e0e0e0", borderRadius: 8,
        padding: 16, marginBottom: 16, background: "#fafafa",
      }}>
        {messages.length === 0 && (
          <p style={{ color: "#999", textAlign: "center", marginTop: 40 }}>
            권한 신청 메시지를 입력하세요<br />
            예: &quot;마케팅 대시보드 read 권한 주세요&quot;
          </p>
        )}
        {messages.map((msg, i) => (
          <div key={i} style={{
            marginBottom: 12,
            display: "flex",
            justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
          }}>
            <div style={{
              maxWidth: "75%",
              padding: "10px 14px",
              borderRadius: msg.role === "user" ? "14px 14px 4px 14px" : "14px 14px 14px 4px",
              background: msg.role === "user" ? "#0070f3" : "#fff",
              color: msg.role === "user" ? "#fff" : "#333",
              border: msg.role === "user" ? "none" : "1px solid #e0e0e0",
              fontSize: 14,
              lineHeight: 1.6,
            }}>
              {msg.role === "agent" && msg.decision && (
                <div style={{
                  display: "inline-block",
                  padding: "2px 8px",
                  borderRadius: 4,
                  marginBottom: 6,
                  fontSize: 12,
                  fontWeight: 700,
                  background: msg.decision === "approve" ? "#d4edda" : msg.decision === "reject" ? "#f8d7da" : "#fff3cd",
                  color: msg.decision === "approve" ? "#155724" : msg.decision === "reject" ? "#721c24" : "#856404",
                }}>
                  {msg.decision === "approve" ? "승인" : msg.decision === "reject" ? "반려" : "에스컬레이션"}
                </div>
              )}
              <div>{msg.content}</div>
              {msg.actions && msg.actions.length > 0 && (
                <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
                  {msg.actions.map((a, j) => (
                    <div key={j}>- {a}</div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ textAlign: "center", color: "#999", fontSize: 14 }}>
            Agent 심사 중...
          </div>
        )}
      </div>

      {/* 입력 영역 */}
      <div style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="권한 신청 메시지를 입력하세요..."
          disabled={loading}
          style={{
            flex: 1, padding: "10px 14px", border: "1px solid #ddd",
            borderRadius: 8, fontSize: 14,
          }}
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          style={{
            padding: "10px 20px", background: "#0070f3", color: "#fff",
            border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14,
            opacity: loading || !input.trim() ? 0.5 : 1,
          }}
        >
          전송
        </button>
      </div>
    </div>
  );
}
