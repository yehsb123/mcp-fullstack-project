"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8001/api/v1";

interface AccessRequest {
  id: number;
  user_id: number;
  resource_name: string;
  access_level: string;
  reason: string;
  status: string;
  created_at: string;
}

export default function AdminPage() {
  const [requests, setRequests] = useState<AccessRequest[]>([]);

  const fetchRequests = async () => {
    const res = await fetch(`${API_BASE}/access-requests`);
    const data = await res.json();
    setRequests(data);
  };

  // --- 승인/반려 처리 (2주차) ---
  // TODO: fetch로 PATCH /api/v1/access-requests/{id} 호출
  // 힌트: fetch(`${API_BASE}/access-requests/${requestId}`, { method: "PATCH", headers: {...}, body: JSON.stringify({ status: newStatus }) })
  const handleStatusChange = async (requestId: number, newStatus: string) => {
    await fetch(`${API_BASE}/access-requests/${requestId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });

    await fetchRequests();
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const pending = requests.filter((r) => r.status === "pending");
  const processed = requests.filter((r) => r.status !== "pending");

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 40 }}>
      <h1>AccessGuard - 관리자</h1>

      {/* 승인 대기 */}
      <section style={{ marginBottom: 40 }}>
        <h2>승인 대기 ({pending.length}건)</h2>
        {pending.length === 0 ? (
          <p style={{ color: "#666" }}>대기 중인 신청이 없습니다.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #ddd" }}>
                <th style={{ padding: 8, textAlign: "left" }}>ID</th>
                <th style={{ padding: 8, textAlign: "left" }}>신청자</th>
                <th style={{ padding: 8, textAlign: "left" }}>리소스</th>
                <th style={{ padding: 8, textAlign: "left" }}>레벨</th>
                <th style={{ padding: 8, textAlign: "left" }}>사유</th>
                <th style={{ padding: 8, textAlign: "left" }}>신청일</th>
                <th style={{ padding: 8, textAlign: "left" }}>처리</th>
              </tr>
            </thead>
            <tbody>
              {pending.map((req) => (
                <tr key={req.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: 8 }}>{req.id}</td>
                  <td style={{ padding: 8 }}>user #{req.user_id}</td>
                  <td style={{ padding: 8 }}>{req.resource_name}</td>
                  <td style={{ padding: 8 }}>{req.access_level}</td>
                  <td style={{ padding: 8, maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{req.reason}</td>
                  <td style={{ padding: 8 }}>{new Date(req.created_at).toLocaleDateString("ko-KR")}</td>
                  <td style={{ padding: 8 }}>
                    <div style={{ display: "flex", gap: 6 }}>
                      <button
                        onClick={() => handleStatusChange(req.id, "approved")}
                        style={{ padding: "4px 12px", background: "#28a745", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 13 }}
                      >
                        승인
                      </button>
                      <button
                        onClick={() => handleStatusChange(req.id, "rejected")}
                        style={{ padding: "4px 12px", background: "#dc3545", color: "#fff", border: "none", borderRadius: 4, cursor: "pointer", fontSize: 13 }}
                      >
                        반려
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* 처리 완료 */}
      <section>
        <h2>처리 완료 ({processed.length}건)</h2>
        {processed.length === 0 ? (
          <p style={{ color: "#666" }}>처리된 신청이 없습니다.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #ddd" }}>
                <th style={{ padding: 8, textAlign: "left" }}>ID</th>
                <th style={{ padding: 8, textAlign: "left" }}>신청자</th>
                <th style={{ padding: 8, textAlign: "left" }}>리소스</th>
                <th style={{ padding: 8, textAlign: "left" }}>레벨</th>
                <th style={{ padding: 8, textAlign: "left" }}>결과</th>
                <th style={{ padding: 8, textAlign: "left" }}>신청일</th>
              </tr>
            </thead>
            <tbody>
              {processed.map((req) => (
                <tr key={req.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: 8 }}>{req.id}</td>
                  <td style={{ padding: 8 }}>user #{req.user_id}</td>
                  <td style={{ padding: 8 }}>{req.resource_name}</td>
                  <td style={{ padding: 8 }}>{req.access_level}</td>
                  <td style={{ padding: 8 }}>
                    <span style={{
                      padding: "2px 8px",
                      borderRadius: 4,
                      background: req.status === "approved" ? "#d4edda" : "#f8d7da",
                      color: req.status === "approved" ? "#155724" : "#721c24",
                    }}>
                      {req.status === "approved" ? "승인" : "반려"}
                    </span>
                  </td>
                  <td style={{ padding: 8 }}>{new Date(req.created_at).toLocaleDateString("ko-KR")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
