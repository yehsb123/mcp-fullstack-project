"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api/v1";

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

const DECISION: Record<string, { label: string; cls: string }> = {
  approve: { label: "승인", cls: "badge-approved" },
  reject: { label: "반려", cls: "badge-rejected" },
  escalate: { label: "에스컬레이션", cls: "badge-escalate" },
};

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

  return (
    <div className="page-body">
      <h1 className="page-title">처리 이력</h1>
      <p className="page-desc">Agent가 처리한 모든 판단 기록을 보여줍니다.</p>

      {loading ? (
        <div className="card"><div className="empty-state">로딩 중...</div></div>
      ) : logs.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            <div className="empty-icon">📝</div>
            처리 이력이 없습니다. AI 채팅에서 권한 신청을 먼저 해보세요.
          </div>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {logs.map((log) => {
            const d = DECISION[log.decision] || DECISION.escalate;
            return (
              <div key={log.id} className="log-card">
                <div className="log-card-header">
                  <div className="log-card-meta">
                    <span className="log-card-id">#{log.id}</span>
                    <span className={`badge ${d.cls}`}>{d.label}</span>
                    <span className="log-card-by">by {log.decided_by}</span>
                  </div>
                  <span className="log-card-time">
                    {log.created_at ? new Date(log.created_at).toLocaleString("ko-KR") : "-"}
                  </span>
                </div>
                <div className="log-card-body">
                  {log.reasoning || "(판단 근거 없음)"}
                </div>
                {log.policy_referenced && (
                  <div className="log-card-policy">참고 정책: {log.policy_referenced}</div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
