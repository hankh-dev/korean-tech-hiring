import Link from "next/link";
import type { Metadata } from "next";
import { getStats } from "@/lib/data";
import { Bar, Card, SectionTitle } from "@/components/ui";

export const metadata: Metadata = {
  title: "직군 분포",
  description: "백엔드, 프론트엔드, ML/AI, DevOps 등 국내 개발 채용 공고의 직군별 분포를 확인하세요.",
};

export default function RolesPage() {
  const stats = getStats();
  const max = stats.roles[0]?.count ?? 1;

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">직군 분포</h1>
        <p className="mt-2 text-sm text-muted">
          개발 공고 {stats.totals.techJobs}건을 직군별로 분류한 결과입니다. 직군을 눌러 해당 공고를 확인하세요.
        </p>
      </header>


      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="divide-y divide-border">
          {stats.roles.map((r) => (
            <Link key={r.slug} href={`/roles/${r.slug}`} className="block px-4 py-3 transition hover:bg-slate-50">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold">{r.name}</span>
                <span className="text-xs text-muted">{r.count}건 · {r.share}%</span>
              </div>
              <div className="mt-2"><Bar value={r.count} max={max} color="bg-accent" /></div>
            </Link>
          ))}
        </Card>

        <div className="grid content-start gap-4">
          <div>
            <SectionTitle title="시니어리티 분포" desc="직함에 표기된 경력 수준 기준" />
            <Card className="divide-y divide-border">
              {stats.seniority.map((s) => (
                <div key={s.key} className="flex items-center justify-between px-4 py-2.5 text-sm">
                  <span className="font-semibold">{s.name}</span>
                  <span className="text-xs text-muted">{s.count}건 · {s.share}%</span>
                </div>
              ))}
            </Card>
          </div>
          <div>
            <SectionTitle title="근무 형태" />
            <Card className="divide-y divide-border">
              {stats.remote.map((r) => (
                <div key={r.key} className="flex items-center justify-between px-4 py-2.5 text-sm">
                  <span className="font-semibold">{r.name}</span>
                  <span className="text-xs text-muted">{r.count}건 · {r.share}%</span>
                </div>
              ))}
            </Card>
          </div>
        </div>
      </div>

      <p className="mt-8 text-xs text-muted">
        직군 분류는 공고 제목 기반 휴리스틱입니다. 제목이 모호한 경우 소프트웨어 엔지니어링으로 분류되며,
        비개발 직무(마케팅·영업·디자인 등)는 집계에서 제외됩니다.
      </p>
    </div>
  );
}
