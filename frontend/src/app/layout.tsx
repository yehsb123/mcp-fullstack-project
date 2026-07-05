import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AccessGuard",
  description: "AI 기반 접근 권한 자동 심사 시스템",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
