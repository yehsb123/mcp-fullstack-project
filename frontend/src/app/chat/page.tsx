"use client";

import { useState } from "react";

const API_BASE = "http://localhost:8000/api/v1";

interface ChatMessage {
  role: "user" | "agent";
  content: string;
  decision?: string;
  actions?: string[];
}

const DECISION_STYLE: Record<string, { label: string; bg: string; color: string }> = {
  approve: { label: "승인", bg: "#ECFDF5", color: "#065F46" },
  reject: { label: "반려", bg: "#FEF2F2", color: "#991B1B" },
  escalate: { label: "에스컬레이션", bg: "#EEF2FF", color: "#4338CA" },
};

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [userId, setUserId] = useState("1");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    if (input.trim().length < 5) {
      setMessages((prev) => [...prev, { role: "agent", content: "5자 이상의 구체적인 권한 신청을 입력해주세요." }]);
      return;
    }

    const userMsg: ChatMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    const messageText = input;
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/agent/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageText, user_id: Number(userId) }),
      });

      if (!res.ok) {
        const errText = await res.text();
        setMessages((prev) => [...prev, { role: "agent", content: `서버 오류 (${res.status}): ${errText}` }]);
        setLoading(false);
        return;
      }

      const data = await res.json();
      setMessages((prev) => [...prev, {
        role: "agent",
        content: data.reasoning,
        decision: data.decision,
        actions: data.actions_taken,
      }]);
    } catch {
      setMessages((prev) => [...prev, { role: "agent", content: "연결 실패: 백엔드(localhost:8000)가 실행 중인지 확인하세요." }]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h1 className="page-title" style={{ marginBottom: 4 }}>AI 권한 심사</h1>
            <p style={{ fontSize: 13, color: "var(--bg1-text)" }}>보안 정책 기반 자동 판단</p>
          </div>
          <div className="chat-user-select">
            <span>사용자 ID</span>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-welcome">
            <div className="chat-welcome-icon">🛡️</div>
            <div className="chat-welcome-title">권한 신청 메시지를 입력하세요</div>
            <div className="chat-welcome-sub">예: "마케팅 대시보드 read 권한 주세요"</div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <div key={i} className={`chat-msg chat-msg-${msg.role}`}>
                <div className={`chat-bubble chat-bubble-${msg.role}`}>
                  {msg.role === "agent" && msg.decision && (() => {
                    const d = DECISION_STYLE[msg.decision] || DECISION_STYLE.escalate;
                    return (
                      <div className="chat-decision-badge" style={{ background: d.bg, color: d.color }}>
                        {d.label}
                      </div>
                    );
                  })()}
                  <div>{msg.content}</div>
                  {msg.actions && msg.actions.length > 0 && (
                    <div className="chat-actions">
                      {msg.actions.map((a, j) => <div key={j}>→ {a}</div>)}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-msg chat-msg-agent">
                <div className="chat-loading">
                  <span className="chat-loading-dot" />
                  <span className="chat-loading-dot" />
                  <span className="chat-loading-dot" />
                  <span style={{ marginLeft: 4 }}>심사 중</span>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      <div className="chat-input-area">
        <div className="chat-input-row">
          <input
            type="text"
            className="form-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="권한 신청 메시지를 입력하세요..."
            disabled={loading}
          />
          <button
            className="btn btn-primary"
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            전송
          </button>
        </div>
      </div>
    </div>
  );
}
