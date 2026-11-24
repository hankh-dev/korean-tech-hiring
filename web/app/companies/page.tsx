import Link from "next/link";
import type { Metadata } from "next";
import { getStats, STACK_NAME } from "@/lib/data";
import { Badge, Card } from "@/components/ui";

export const metadata: Metadata = {
  title: "기업별 채용 현황",
  description: "국내에서 개발자를 채용 중인 기업별 공고 수, AI 공고, 주요 기술 스택을 확인하세요.",
};

export default function CompaniesPage() {
  const stats = getStats();
  const korean = stats.companies.filter((c) => c.type === "korean");
  const global = stats.companies.filter((c) => c.type !== "korean");

  const renderCard = (c: (typeof stats.companies)[number]) => (
    <Link key={c.slug} href={`/companies/${c.slug}`}>
      <Card className="h-full p-5 transition hover:border-primary/40 hover:shadow-sm">
        <div className="flex items-center justify-between gap-2">
          <span className="text-lg font-extrabold">{c.name}</span>
          <Badge tone={c.type === "korean" ? "korean" : "global"}>
            {c.type === "korean" ? "국내" : "글로벌"}
          </Badge>
        </div>
        <p className="mt-1 line-clamp-2 text-xs leading-relaxed text-muted">{c.description}</p>
        <div className="mt-4 flex items-end gap-4">
          <div>
            <p className="text-2xl font-extrabold">{c.jobCount}</p>
            <p className="text-[11px] text-muted">개발 공고</p>
          </div>
          <div>
            <p className="text-2xl font-extrabold text-violet-600">{c.aiCount}</p>
            <p className="text-[11px] text-muted">AI 관련</p>
          </div>
          <div>
            <p className="text-2xl font-extrabold text-emerald-600">{c.posted7d}</p>
            <p className="text-[11px] text-muted">신규 7일</p>
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-1">
          {c.topStacks.slice(0, 4).map((s) => (
            <span key={s.slug} className="rounded-md bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600">
              {STACK_NAME[s.slug] ?? s.name}
            </span>
          ))}
        </div>
      </Card>
    </Link>
  );

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">기업별 채용 현황</h1>
        <p className="mt-2 text-sm text-muted">
          개발 직군 공고가 게시된 {stats.companies.length}개 기업입니다. 기업을 눌러 상세 공고와 기술 스택을 확인하세요.
        </p>
      </header>


      <section className="mt-6">
        <h2 className="mb-3 text-lg font-bold">국내 기업 <span className="text-sm font-medium text-muted">{korean.length}곳</span></h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{korean.map(renderCard)}</div>
      </section>

      <section className="mt-10">
        <h2 className="mb-3 text-lg font-bold">글로벌 기업 (한국 채용) <span className="text-sm font-medium text-muted">{global.length}곳</span></h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{global.map(renderCard)}</div>
      </section>
    </div>
  );
}
