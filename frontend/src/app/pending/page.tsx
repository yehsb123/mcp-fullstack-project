"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api/v1";

interface AccessRequest {
  id: number;
  user_id: number;
  resource_name: string;
  access_level: string;
  status: string;
  reason: string | null;
  created_at: string;
}

export default function PendingPage() {
  const [requests, setRequests] = useState<AccessRequest[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchPending = async () => {
    setLoading(true);
    const res = await fetch(`${API_BASE}/access-requests`);
    const data: AccessRequest[] = await res.json();
    const pending = data.filter((r) => r.status === "pending");
    setRequests(pending);
    setLoading(false);
  };

  useEffect(() => {
    fetchPending();
  }, []);

  const handleAction = async (id: number, status: "approved" | "rejected") => {
    await fetch(`${API_BASE}/access-requests/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    fetchPending();
  };

  const statusLabel: Record<string, string> = {
    pending: "대기중",
    approved: "승인",
    rejected: "반려",
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 40 }}>
      <h1 style={{ marginBottom: 8 }}>승인 대기 목록</h1>
      <p style={{ color: "#666", marginBottom: 24, fontSize: 14 }}>
        현재 대기중(pending)인 권한 신청 건만 표시됩니다.
      </p>

      {loading ? (
        <p style={{ color: "#999" }}>로딩 중...</p>
      ) : requests.length === 0 ? (
        <p style={{ color: "#999", textAlign: "center", marginTop: 40 }}>
          대기중인 신청이 없습니다.
        </p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #e0e0e0", textAlign: "left" }}>
              <th style={{ padding: "8px 12px" }}>#</th>
              <th style={{ padding: "8px 12px" }}>신청자 ID</th>
              <th style={{ padding: "8px 12px" }}>리소스</th>
              <th style={{ padding: "8px 12px" }}>레벨</th>
              <th style={{ padding: "8px 12px" }}>사유</th>
              <th style={{ padding: "8px 12px" }}>상태</th>
              <th style={{ padding: "8px 12px" }}>처리</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                <td style={{ padding: "8px 12px" }}>{r.id}</td>
                <td style={{ padding: "8px 12px" }}>{r.user_id}</td>
                <td style={{ padding: "8px 12px" }}>{r.resource_name}</td>
                <td style={{ padding: "8px 12px" }}>{r.access_level}</td>
                <td style={{ padding: "8px 12px", maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {r.reason || "-"}
                </td>
                <td style={{ padding: "8px 12px" }}>
                  <span style={{ padding: "2px 8px", borderRadius: 4, fontSize: 12, fontWeight: 700, background: "#fff3cd", color: "#856404" }}>
                    {statusLabel[r.status] || r.status}
                  </span>
                </td>
                <td style={{ padding: "8px 12px", display: "flex", gap: 4 }}>
                  <button
                    onClick={() => handleAction(r.id, "approved")}
                    style={{ padding: "4px 12px", background: "#28a745", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 12 }}
                  >
                    승인
                  </button>
                  <button
                    onClick={() => handleAction(r.id, "rejected")}
                    style={{ padding: "4px 12px", background: "#dc3545", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 12 }}
                  >
                    반려
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div style={{ marginTop: 24 }}>
        <a href="/" style={{ color: "#0070f3", fontSize: 14 }}>← 메인으로</a>
        {" | "}
        <a href="/chat" style={{ color: "#0070f3", fontSize: 14 }}>AI 채팅</a>
        {" | "}
        <a href="/audit-logs" style={{ color: "#0070f3", fontSize: 14 }}>처리 이력</a>
      </div>
    </div>
  );
}
