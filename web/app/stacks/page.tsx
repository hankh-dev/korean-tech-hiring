import Link from "next/link";
import type { Metadata } from "next";
import { getStats } from "@/lib/data";
import { Bar, Badge, Card, DeltaBadge, SectionTitle } from "@/components/ui";

export const metadata: Metadata = {
  title: "기술 스택 분석",
  description: "국내 개발 채용 공고에서 가장 많이 요구되는 기술 스택 순위와 주간 변화를 확인하세요.",
};

export default function StacksPage() {
  const stats = getStats();
  const categories = Array.from(new Set(stats.stacks.map((s) => s.category)));
  const maxCount = stats.stacks[0]?.count ?? 1;

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">기술 스택 분석</h1>
        <p className="mt-2 text-sm text-muted">
          개발 공고 {stats.totals.techJobs}건에서 추출한 {stats.totals.stacks}개 기술의 언급 빈도입니다.
          ▲▼는 최근 7일 신규 공고에서의 전주 대비 변화입니다.
        </p>
      </header>


      {categories.map((category) => {
        const rows = stats.stacks.filter((s) => s.category === category);
        if (rows.length === 0) return null;
        return (
          <section key={category} className="mt-8">
            <SectionTitle title={category} desc={`${rows.length}개 기술`} />
            <Card className="divide-y divide-border">
              {rows.map((s) => (
                <Link
                  key={s.slug}
                  href={`/stacks/${s.slug}`}
                  className="flex items-center gap-4 px-4 py-3 transition hover:bg-slate-50"
                >
                  <div className="w-32 shrink-0 sm:w-44">
                    <p className="truncate text-sm font-bold">{s.name}</p>
                    <p className="truncate text-[11px] text-muted">{s.blurb}</p>
                  </div>
                  <div className="min-w-0 flex-1">
                    <Bar value={s.count} max={maxCount} />
                  </div>
                  <div className="flex w-36 shrink-0 items-center justify-end gap-2 text-xs text-muted">
                    <DeltaBadge delta={s.delta7d} />
                    <span className="font-semibold text-foreground">{s.count}건</span>
                    <span>{s.share}%</span>
                  </div>
                </Link>
              ))}
            </Card>
          </section>
        );
      })}

      <p className="mt-8 text-xs text-muted">
        <Badge>집계 기준</Badge> 공고 제목·본문에 기술명이 명시적으로 언급된 경우만 집계합니다.
        한 공고에 여러 기술이 언급되면 각각 카운트하므로 비중 합은 100%를 넘을 수 있습니다.
      </p>
    </div>
  );
}
