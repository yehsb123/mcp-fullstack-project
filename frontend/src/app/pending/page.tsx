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
    setRequests(data.filter((r) => r.status === "pending"));
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

  return (
    <div className="page-body">
      <h1 className="page-title">승인 대기</h1>
      <p className="page-desc">현재 대기중(pending)인 권한 신청 건만 표시됩니다.</p>

      <div className="card">
        {loading ? (
          <div className="empty-state">로딩 중...</div>
        ) : requests.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">✅</div>
            대기중인 신청이 없습니다.
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>신청자 ID</th>
                  <th>리소스</th>
                  <th>레벨</th>
                  <th>사유</th>
                  <th>상태</th>
                  <th>처리</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((r) => (
                  <tr key={r.id}>
                    <td>{r.id}</td>
                    <td>{r.user_id}</td>
                    <td style={{ fontWeight: 500 }}>{r.resource_name}</td>
                    <td>{r.access_level}</td>
                    <td style={{ maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {r.reason || "-"}
                    </td>
                    <td><span className="badge badge-pending">대기중</span></td>
                    <td>
                      <div style={{ display: "flex", gap: 6 }}>
                        <button className="btn btn-approve" onClick={() => handleAction(r.id, "approved")}>승인</button>
                        <button className="btn btn-reject" onClick={() => handleAction(r.id, "rejected")}>반려</button>
                      </div>
                    </td>
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
