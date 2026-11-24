import Link from "next/link";
import type { Metadata } from "next";
import { getReports } from "@/lib/data";
import { Badge, Card } from "@/components/ui";

export const metadata: Metadata = {
  title: "주간 채용 리포트",
  description: "매주 국내 개발 채용 공고의 스택·직군·AI 비중 변화를 요약한 주간 리포트입니다.",
};

export default function ReportsPage() {
  const reports = getReports();

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">주간 채용 리포트</h1>
        <p className="mt-2 text-sm text-muted">
          매주 게시된 신규 공고를 기준으로 스택·직군·AI 비중을 요약합니다. 리포트를 눌러 상세 내용을 확인하세요.
        </p>
      </header>


      <div className="grid gap-4">
        {reports.map((r) => (
          <Link key={r.slug} href={`/reports/${r.slug}`}>
            <Card className="p-5 transition hover:border-primary/40 hover:shadow-sm">
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-bold">{r.title}</h2>
                {r.partial ? <Badge tone="hybrid">진행 중</Badge> : null}
              </div>
              <p className="mt-2 text-sm leading-relaxed text-muted">{r.summary}</p>
              <div className="mt-3 flex flex-wrap gap-2 text-xs">
                <Badge tone="primary">신규 {r.stats.jobs}건</Badge>
                <Badge tone="ai">AI {r.stats.aiShare}%</Badge>
                <Badge tone="remote">원격·하이브리드 {r.stats.remoteShare}%</Badge>
                {r.stats.topStacks.slice(0, 3).map((s) => (
                  <Badge key={s.slug}>{s.name} {s.count}</Badge>
                ))}
              </div>
            </Card>
          </Link>
        ))}
        {reports.length === 0 ? (
          <Card className="p-10 text-center text-sm text-muted">아직 생성된 리포트가 없습니다.</Card>
        ) : null}
      </div>
    </div>
  );
}
