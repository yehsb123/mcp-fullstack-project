"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";

const NAV_ITEMS = [
  { href: "/", label: "권한 신청" },
  { href: "/chat", label: "AI 채팅" },
  { href: "/admin", label: "관리자" },
  { href: "/pending", label: "승인 대기" },
  { href: "/audit-logs", label: "처리 이력" },
];

export default function Navigation() {
  const pathname = usePathname();

  return (
    <header className="app-header">
      <div className="header-accent" />
      <div className="header-inner">
        <Link href="/" className="header-brand">
          <span className="brand-icon">AG</span>
          AccessGuard
        </Link>
        <nav className="header-nav">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-link${pathname === item.href ? " active" : ""}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
