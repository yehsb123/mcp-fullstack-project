"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8001/api/v1";

interface AuditLog {
  id: number;
  request_id: number;
  action: string;
  decision: string;
  reasoning: string;
  policy_referenced: string;
  decided_by: string;
  created_at: string | null;
}

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      const res = await fetch(`${API_BASE}/audit-logs`);
      const data = await res.json();
      setLogs(data);
      setLoading(false);
    };
    fetchLogs();
  }, []);

  const decisionStyle = (decision: string) => {
    if (decision === "approve")
      return { background: "#d4edda", color: "#155724" };
    if (decision === "reject")
      return { background: "#f8d7da", color: "#721c24" };
    return { background: "#fff3cd", color: "#856404" };
  };

  const decisionLabel = (decision: string) => {
    if (decision === "approve") return "승인";
    if (decision === "reject") return "반려";
    return "에스컬레이션";
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 40 }}>
      <h1 style={{ marginBottom: 8 }}>처리 이력 조회</h1>
      <p style={{ color: "#666", marginBottom: 24, fontSize: 14 }}>
        Agent가 처리한 모든 판단 기록을 보여줍니다.
      </p>

      {loading ? (
        <p style={{ color: "#999" }}>로딩 중...</p>
      ) : logs.length === 0 ? (
        <p style={{ color: "#999", textAlign: "center", marginTop: 40 }}>
          처리 이력이 없습니다. AI 채팅에서 권한 신청을 먼저 해보세요.
        </p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {logs.map((log) => (
            <div
              key={log.id}
              style={{
                border: "1px solid #e0e0e0",
                borderRadius: 8,
                padding: 16,
                background: "#fafafa",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontWeight: 700, fontSize: 14 }}>
                    #{log.id}
                  </span>
                  <span
                    style={{
                      padding: "2px 8px",
                      borderRadius: 4,
                      fontSize: 12,
                      fontWeight: 700,
                      ...decisionStyle(log.decision),
                    }}
                  >
                    {decisionLabel(log.decision)}
                  </span>
                  <span style={{ fontSize: 12, color: "#999" }}>
                    by {log.decided_by}
                  </span>
                </div>
                <span style={{ fontSize: 12, color: "#999" }}>
                  {log.created_at
                    ? new Date(log.created_at).toLocaleString("ko-KR")
                    : "-"}
                </span>
              </div>
              <div style={{ fontSize: 14, lineHeight: 1.6, color: "#333" }}>
                {log.reasoning || "(판단 근거 없음)"}
              </div>
              {log.policy_referenced && (
                <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
                  참고 정책: {log.policy_referenced}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: 24 }}>
        <a href="/" style={{ color: "#0070f3", fontSize: 14 }}>← 메인으로</a>
        {" | "}
        <a href="/chat" style={{ color: "#0070f3", fontSize: 14 }}>AI 채팅</a>
        {" | "}
        <a href="/pending" style={{ color: "#0070f3", fontSize: 14 }}>승인 대기</a>
      </div>
    </div>
  );
}
