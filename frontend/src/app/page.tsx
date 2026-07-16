"use client";

import { useState, useEffect } from "react";

// FastAPI 백엔드 주소
const API_BASE = "http://localhost:8000/api/v1";

// --- 타입 정의 ---
interface AccessRequest {
  id: number;
  user_id: number;
  resource_name: string;
  access_level: string;
  reason: string;
  status: string;
  created_at: string;
}

export default function Home() {
  // --- 상태 ---
  const [requests, setRequests] = useState<AccessRequest[]>([]);
  const [loading, setLoading] = useState(false);

  // 폼 입력값
  const [userId, setUserId] = useState("");
  const [resourceName, setResourceName] = useState("");
  const [accessLevel, setAccessLevel] = useState("read");
  const [reason, setReason] = useState("");

  // --- 신청 목록 조회 ---
  //fetch로 GET /api/v1/access-requests 호출
  // 힌트: fetch(`${API_BASE}/access-requests`).then(res => res.json()).then(data => setRequests(data))
  const fetchRequests = async () => {
    const res = await fetch(`${API_BASE}/access-requests`);
    const data = await res.json();
    setRequests(data);
  };

  // --- 권한 신청 ---
  //  fetch로 POST /api/v1/access-requests 호출
  // 힌트: fetch(`${API_BASE}/access-requests`, { method: "POST", headers: {...}, body: JSON.stringify({...}) })
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setLoading(true);

    await fetch(`${API_BASE}/access-requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: Number(userId),
        resource_name: resourceName,
        access_level: accessLevel,
        reason: reason,
      }),
    });

    setLoading(false);
    setResourceName("");
    setReason("");
    await fetchRequests();
  };

  // 페이지 로드 시 목록 조회
  useEffect(() => {
    fetchRequests();
  }, []);

  // --- UI (멘토 제공) ---
  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 40 }}>
      <h1>AccessGuard - 권한 신청</h1>

      {/* 신청 폼 */}
      <section style={{ marginBottom: 40, padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
        <h2>새 권한 신청</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 12 }}>
            <label>사용자 ID: </label>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="1"
              required
              style={{ padding: 8, width: 200 }}
            />
          </div>
          <div style={{ marginBottom: 12 }}>
            <label>리소스 이름: </label>
            <input
              type="text"
              value={resourceName}
              onChange={(e) => setResourceName(e.target.value)}
              placeholder="마케팅 대시보드"
              required
              style={{ padding: 8, width: 200 }}
            />
          </div>
          <div style={{ marginBottom: 12 }}>
            <label>접근 레벨: </label>
            <select
              value={accessLevel}
              onChange={(e) => setAccessLevel(e.target.value)}
              style={{ padding: 8 }}
            >
              <option value="read">읽기 (Read)</option>
              <option value="write">쓰기 (Write)</option>
              <option value="admin">관리자 (Admin)</option>
            </select>
          </div>
          <div style={{ marginBottom: 12 }}>
            <label>신청 사유: </label>
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="권한이 필요한 이유를 적어주세요"
              required
              style={{ padding: 8, width: "100%", minHeight: 60 }}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            style={{ padding: "10px 24px", background: "#0070f3", color: "#fff", border: "none", borderRadius: 6, cursor: "pointer" }}
          >
            {loading ? "신청 중..." : "권한 신청"}
          </button>
        </form>
      </section>

      {/* 신청 목록 */}
      <section>
        <h2>신청 목록</h2>
        {requests.length === 0 ? (
          <p style={{ color: "#666" }}>신청 내역이 없습니다.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #ddd" }}>
                <th style={{ padding: 8, textAlign: "left" }}>ID</th>
                <th style={{ padding: 8, textAlign: "left" }}>리소스</th>
                <th style={{ padding: 8, textAlign: "left" }}>레벨</th>
                <th style={{ padding: 8, textAlign: "left" }}>상태</th>
                <th style={{ padding: 8, textAlign: "left" }}>신청일</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((req) => (
                <tr key={req.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: 8 }}>{req.id}</td>
                  <td style={{ padding: 8 }}>{req.resource_name}</td>
                  <td style={{ padding: 8 }}>{req.access_level}</td>
                  <td style={{ padding: 8 }}>
                    <span style={{
                      padding: "2px 8px",
                      borderRadius: 4,
                      background: req.status === "approved" ? "#d4edda" : req.status === "rejected" ? "#f8d7da" : "#fff3cd",
                      color: req.status === "approved" ? "#155724" : req.status === "rejected" ? "#721c24" : "#856404",
                    }}>
                      {req.status === "pending" ? "대기중" : req.status === "approved" ? "승인" : "반려"}
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
