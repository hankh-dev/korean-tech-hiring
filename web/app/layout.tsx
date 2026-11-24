import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";
import { Nav } from "@/components/nav";

export const metadata: Metadata = {
  title: {
    default: "개발자 채용 데이터랩 — 국내 테크 채용 데이터 분석",
    template: "%s | 개발자 채용 데이터랩",
  },
  description:
    "쿠팡·당근·크래프톤 등 국내에서 채용 중인 테크 기업의 개발 공고를 매일 수집해 기술 스택, 직군, 기업별 채용 동향을 분석합니다.",
  keywords: ["개발자 채용", "테크 채용", "기술 스택", "채용 트렌드", "개발자 커리어"],
  openGraph: {
    title: "개발자 채용 데이터랩",
    description: "국내 테크 기업 개발 채용 공고를 데이터로 분석합니다.",
    locale: "ko_KR",
    type: "website",
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
        />
      </head>
      <body className="font-sans">
        <Nav />
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
        <footer className="border-t border-border bg-card">
          <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-sm text-muted sm:flex-row sm:items-center sm:justify-between">
            <p>
              © 2026 개발자 채용 데이터랩 · 공개 채용 보드 기반 자동 집계 · 매일 갱신
            </p>
            <div className="flex gap-4">
              <Link href="/about" className="hover:text-foreground">소개·방법론</Link>
              <Link href="/privacy" className="hover:text-foreground">개인정보처리방침</Link>
              <Link href="/reports" className="hover:text-foreground">주간 리포트</Link>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
