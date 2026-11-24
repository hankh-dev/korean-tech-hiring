import Link from "next/link";
import {
  Briefcase,
  Building2,
  CalendarPlus,
  Cpu,
  Globe2,
  Sparkles,
} from "lucide-react";
import { getStats, num, formatDateTime, STACK_NAME } from "@/lib/data";
import { Bar, Badge, Card, SectionTitle, StatCard, DeltaBadge } from "@/components/ui";
import { WeeklyBars, DailySpark } from "@/components/charts";
import { JobCard } from "@/components/job-card";

export default function DashboardPage() {
  const stats = getStats();
  const t = stats.totals;
  const topStacks = stats.stacks.slice(0, 10);
  const maxStack = topStacks[0]?.count ?? 1;
  const maxRole = stats.roles[0]?.count ?? 1;
  const topCompanies = stats.companies.slice(0, 6);

  return (
    <div>
      <section className="mb-8">
        <div className="flex flex-wrap items-center gap-2">
          <Badge tone="primary">매일 자동 갱신</Badge>
          <Badge>공개 ATS 보드 {stats.meta.boardCount}곳</Badge>
        </div>
        <h1 className="mt-3 text-3xl font-extrabold tracking-tight sm:text-4xl">
          개발자 채용 데이터랩
        </h1>
        <p className="mt-2 max-w-2xl text-[15px] leading-relaxed text-muted">
          국내에서 채용 중인 테크 기업의 개발 공고를 매일 수집해{" "}
          <strong className="text-foreground">기술 스택 · 직군 · 기업별 동향</strong>을
          분석합니다. 어떤 기술을 배우면 좋을지, 데이터로 확인하세요.
        </p>
        <p className="mt-2 text-xs text-muted">
          마지막 갱신: {formatDateTime(stats.generatedAt)} (KST 기준 집계)
        </p>
      </section>

      <section className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <StatCard label="개발 공고" value={num(t.techJobs)} unit="건" icon={<Briefcase className="h-4 w-4" />} hint={`전체 한국 공고 ${num(t.allKoreaJobs)}건 중`} />
        <StatCard label="채용 기업" value={num(t.companies)} unit="곳" icon={<Building2 className="h-4 w-4" />} hint="개발 직군 채용 중인 기업" />
        <StatCard label="AI 관련" value={num(t.aiJobs)} unit="건" icon={<Sparkles className="h-4 w-4" />} hint={`전체의 ${Math.round((t.aiJobs / Math.max(1, t.techJobs)) * 100)}%`} />
        <StatCard label="신규 7일" value={num(t.new7d)} unit="건" icon={<CalendarPlus className="h-4 w-4" />} hint={`최근 30일 ${num(t.new30d)}건`} />
        <StatCard label="원격·하이브리드" value={num(t.remoteJobs + t.hybridJobs)} unit="건" icon={<Globe2 className="h-4 w-4" />} hint={`원격 ${t.remoteJobs} · 하이브리드 ${t.hybridJobs}`} />
      </section>


      <section className="grid gap-6 lg:grid-cols-2">
        <div>
          <SectionTitle
            title="많이 요구되는 기술 스택 Top 10"
            desc="공고 원문에서 추출한 기술 언급 기준"
            action={<Link href="/stacks" className="text-sm font-semibold text-primary hover:underline">전체 보기 →</Link>}
          />
          <Card className="divide-y divide-border">
            {topStacks.map((s, i) => (
              <Link key={s.slug} href={`/stacks/${s.slug}`} className="flex items-center gap-3 px-4 py-3 transition hover:bg-slate-50">
                <span className="w-5 text-right text-sm font-bold text-muted">{i + 1}</span>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate text-sm font-semibold">{s.name}</span>
                    <span className="flex items-center gap-2 text-xs text-muted">
                      <DeltaBadge delta={s.delta7d} />
                      {s.count}건 · {s.share}%
                    </span>
                  </div>
                  <div className="mt-1.5"><Bar value={s.count} max={maxStack} /></div>
                </div>
              </Link>
            ))}
          </Card>
        </div>

        <div>
          <SectionTitle
            title="직군 분포"
            desc="개발 공고의 직군별 비중"
            action={<Link href="/roles" className="text-sm font-semibold text-primary hover:underline">전체 보기 →</Link>}
          />
          <Card className="divide-y divide-border">
            {stats.roles.slice(0, 10).map((r) => (
              <Link key={r.slug} href={`/roles/${r.slug}`} className="flex items-center gap-3 px-4 py-3 transition hover:bg-slate-50">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate text-sm font-semibold">{r.name}</span>
                    <span className="text-xs text-muted">{r.count}건 · {r.share}%</span>
                  </div>
                  <div className="mt-1.5"><Bar value={r.count} max={maxRole} color="bg-accent" /></div>
                </div>
              </Link>
            ))}
          </Card>
        </div>
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <div>
          <SectionTitle title="주간 신규 공고 추이" desc="최근 8주, 주별 신규 게시 공고" />
          <Card className="p-4"><WeeklyBars weeks={stats.weekly} /></Card>
        </div>
        <div>
          <SectionTitle title="최근 30일 일별 신규 공고" desc="하루 단위 게시 추이" />
          <Card className="p-4">
            <DailySpark days={stats.dailyNew} />
            <div className="mt-3 grid grid-cols-3 gap-2 text-center">
              {stats.remote.map((r) => (
                <div key={r.key} className="rounded-lg bg-slate-50 px-2 py-2">
                  <p className="text-xs text-muted">{r.name}</p>
                  <p className="text-sm font-bold">{r.count}건 · {r.share}%</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </section>


      <section className="mt-8">
        <SectionTitle
          title="채용 활발 기업"
          desc="개발 공고 수 기준 상위 기업"
          action={<Link href="/companies" className="text-sm font-semibold text-primary hover:underline">전체 보기 →</Link>}
        />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {topCompanies.map((c) => (
            <Link key={c.slug} href={`/companies/${c.slug}`}>
              <Card className="h-full p-4 transition hover:border-primary/40 hover:shadow-sm">
                <div className="flex items-center justify-between">
                  <span className="font-bold">{c.name}</span>
                  <Badge tone={c.type === "korean" ? "korean" : "global"}>
                    {c.type === "korean" ? "국내" : "글로벌"}
                  </Badge>
                </div>
                <p className="mt-1 line-clamp-1 text-xs text-muted">{c.description}</p>
                <p className="mt-3 text-sm">
                  <strong className="text-lg font-extrabold">{c.jobCount}</strong>
                  <span className="text-muted">건 채용</span>
                  {c.aiCount > 0 ? <span className="ml-2 text-xs text-violet-600">AI {c.aiCount}건</span> : null}
                </p>
                <div className="mt-2 flex flex-wrap gap-1">
                  {c.topStacks.slice(0, 3).map((s) => (
                    <span key={s.slug} className="rounded-md bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600">
                      {STACK_NAME[s.slug] ?? s.name}
                    </span>
                  ))}
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-8">
        <SectionTitle
          title="최근 게시 공고"
          desc="가장 최근에 올라온 개발 공고"
          action={<Link href="/jobs" className="text-sm font-semibold text-primary hover:underline">전체 공고 →</Link>}
        />
        <div className="grid gap-3 lg:grid-cols-2">
          {stats.recentJobs.slice(0, 8).map((job) => (
            <JobCard key={job.id} job={job} />
          ))}
        </div>
      </section>
    </div>
  );
}
