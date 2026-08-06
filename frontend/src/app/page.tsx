"use client";

import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api/v1";

interface AccessRequest {
  id: number;
  user_id: number;
  resource_name: string;
  access_level: string;
  reason: string;
  status: string;
  created_at: string;
}

const STATUS: Record<string, { label: string; cls: string }> = {
  pending: { label: "대기중", cls: "badge-pending" },
  approved: { label: "승인", cls: "badge-approved" },
  rejected: { label: "반려", cls: "badge-rejected" },
};

export default function Home() {
  const [requests, setRequests] = useState<AccessRequest[]>([]);
  const [loading, setLoading] = useState(false);

  const [userId, setUserId] = useState("");
  const [resourceName, setResourceName] = useState("");
  const [accessLevel, setAccessLevel] = useState("read");
  const [reason, setReason] = useState("");

  const fetchRequests = async () => {
    const res = await fetch(`${API_BASE}/access-requests`);
    const data = await res.json();
    setRequests(data);
  };

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

  return (
    <div className="page-body">
      <h1 className="page-title">권한 신청</h1>
      <p className="page-desc">리소스 접근 권한을 신청하고 처리 현황을 확인합니다.</p>

      <div className="card section-gap">
        <div className="card-title">새 권한 신청</div>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">사용자 ID</label>
              <input
                type="number"
                className="form-input"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="1"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">리소스 이름</label>
              <input
                type="text"
                className="form-input"
                value={resourceName}
                onChange={(e) => setResourceName(e.target.value)}
                placeholder="마케팅 대시보드"
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">접근 레벨</label>
            <select
              className="form-select"
              value={accessLevel}
              onChange={(e) => setAccessLevel(e.target.value)}
            >
              <option value="read">읽기 (Read)</option>
              <option value="write">쓰기 (Write)</option>
              <option value="admin">관리자 (Admin)</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">신청 사유</label>
            <textarea
              className="form-textarea"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="권한이 필요한 이유를 적어주세요"
              required
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "신청 중..." : "권한 신청"}
          </button>
        </form>
      </div>

      <div className="card">
        <div className="card-title">신청 목록</div>
        {requests.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📋</div>
            신청 내역이 없습니다.
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>리소스</th>
                  <th>레벨</th>
                  <th>상태</th>
                  <th>신청일</th>
                  <th>처리</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((req) => {
                  const s = STATUS[req.status] || STATUS.pending;
                  return (
                    <tr key={req.id}>
                      <td>{req.id}</td>
                      <td style={{ fontWeight: 500 }}>{req.resource_name}</td>
                      <td>{req.access_level}</td>
                      <td><span className={`badge ${s.cls}`}>{s.label}</span></td>
                      <td>{new Date(req.created_at).toLocaleDateString("ko-KR")}</td>
                      <td>
                        {req.status === "pending" ? (
                          <div style={{ display: "flex", gap: 6 }}>
                            <button className="btn btn-approve" onClick={() => handleStatusChange(req.id, "approved")}>승인</button>
                            <button className="btn btn-reject" onClick={() => handleStatusChange(req.id, "rejected")}>반려</button>
                          </div>
                        ) : (
                          <span style={{ color: "var(--muted-faint)", fontSize: 13 }}>처리완료</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
