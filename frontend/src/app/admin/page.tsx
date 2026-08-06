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

export default function AdminPage() {
  const [requests, setRequests] = useState<AccessRequest[]>([]);

  const fetchRequests = async () => {
    const res = await fetch(`${API_BASE}/access-requests`);
    const data = await res.json();
    setRequests(data);
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

  const pending = requests.filter((r) => r.status === "pending");
  const approved = requests.filter((r) => r.status === "approved");
  const rejected = requests.filter((r) => r.status === "rejected");

  return (
    <div className="page-body">
      <h1 className="page-title">관리자 대시보드</h1>
      <p className="page-desc">전체 권한 신청 현황을 한눈에 확인하고 처리합니다.</p>

      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{requests.length}</div>
          <div className="stat-label">전체 신청</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--bi-01)" }}>{pending.length}</div>
          <div className="stat-label">대기중</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--success-modal)" }}>{approved.length}</div>
          <div className="stat-label">승인</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--failure)" }}>{rejected.length}</div>
          <div className="stat-label">반려</div>
        </div>
      </div>

      <div className="card section-gap">
        <div className="card-title">승인 대기 ({pending.length}건)</div>
        {pending.length === 0 ? (
          <div className="empty-state">대기 중인 신청이 없습니다.</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>신청자</th>
                  <th>리소스</th>
                  <th>레벨</th>
                  <th>사유</th>
                  <th>신청일</th>
                  <th>처리</th>
                </tr>
              </thead>
              <tbody>
                {pending.map((req) => (
                  <tr key={req.id}>
                    <td>{req.id}</td>
                    <td>user #{req.user_id}</td>
                    <td style={{ fontWeight: 500 }}>{req.resource_name}</td>
                    <td>{req.access_level}</td>
                    <td style={{ maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{req.reason}</td>
                    <td>{new Date(req.created_at).toLocaleDateString("ko-KR")}</td>
                    <td>
                      <div style={{ display: "flex", gap: 6 }}>
                        <button className="btn btn-approve" onClick={() => handleStatusChange(req.id, "approved")}>승인</button>
                        <button className="btn btn-reject" onClick={() => handleStatusChange(req.id, "rejected")}>반려</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-title">처리 완료 ({approved.length + rejected.length}건)</div>
        {approved.length + rejected.length === 0 ? (
          <div className="empty-state">처리된 신청이 없습니다.</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>신청자</th>
                  <th>리소스</th>
                  <th>레벨</th>
                  <th>결과</th>
                  <th>신청일</th>
                </tr>
              </thead>
              <tbody>
                {[...approved, ...rejected].map((req) => (
                  <tr key={req.id}>
                    <td>{req.id}</td>
                    <td>user #{req.user_id}</td>
                    <td style={{ fontWeight: 500 }}>{req.resource_name}</td>
                    <td>{req.access_level}</td>
                    <td>
                      <span className={`badge ${req.status === "approved" ? "badge-approved" : "badge-rejected"}`}>
                        {req.status === "approved" ? "승인" : "반려"}
                      </span>
                    </td>
                    <td>{new Date(req.created_at).toLocaleDateString("ko-KR")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
