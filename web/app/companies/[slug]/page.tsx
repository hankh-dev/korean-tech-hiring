import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { ExternalLink } from "lucide-react";
import { getCompany, getStats, jobsByCompany, STACK_NAME, formatDate } from "@/lib/data";
import { Badge, Card, SectionTitle, StatCard } from "@/components/ui";
import { JobCard } from "@/components/job-card";
import { Briefcase, CalendarPlus, Globe2, Sparkles } from "lucide-react";

export function generateStaticParams() {
  return getStats().companies.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const company = getCompany(slug);
  if (!company) return {};
  return {
    title: `${company.name} 개발자 채용`,
    description: `${company.name}의 국내 개발 공고 ${company.jobCount}건. 요구 기술 스택과 직군별 공고를 확인하세요.`,
  };
}

export default async function CompanyDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const company = getCompany(slug);
  if (!company) notFound();

  const jobs = jobsByCompany(slug);
  const stackCounts = new Map<string, number>();
  for (const j of jobs) for (const s of j.stacks) stackCounts.set(s, (stackCounts.get(s) ?? 0) + 1);
  const topStacks = Array.from(stackCounts.entries()).sort((a, b) => b[1] - a[1]).slice(0, 12);

  return (
    <div>
      <nav className="mb-4 text-sm text-muted">
        <Link href="/companies" className="hover:text-primary">기업</Link>
        <span className="mx-2">/</span>
        <span className="font-semibold text-foreground">{company.name}</span>
      </nav>

      <header className="mb-6">
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">{company.name}</h1>
          <Badge tone={company.type === "korean" ? "korean" : "global"}>
            {company.type === "korean" ? "국내 기업" : "글로벌 기업"}
          </Badge>
        </div>
        <p className="mt-2 text-sm text-muted">{company.description}</p>
        <div className="mt-3 flex gap-3 text-sm">
          <a href={company.careers} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 font-semibold text-primary hover:underline">
            채용 페이지 <ExternalLink className="h-3.5 w-3.5" />
          </a>
          <a href={company.homepage} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-muted hover:text-foreground">
            홈페이지 <ExternalLink className="h-3.5 w-3.5" />
          </a>
        </div>
      </header>

      <section className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <StatCard label="개발 공고" value={`${company.jobCount}`} unit="건" icon={<Briefcase className="h-4 w-4" />} />
        <StatCard label="AI 관련" value={`${company.aiCount}`} unit="건" icon={<Sparkles className="h-4 w-4" />} />
        <StatCard label="신규 7일" value={`${company.posted7d}`} unit="건" icon={<CalendarPlus className="h-4 w-4" />} hint={`최근 게시 ${formatDate(company.latestPostedAt)}`} />
        <StatCard label="원격·하이브리드" value={`${company.remoteCount}`} unit="건" icon={<Globe2 className="h-4 w-4" />} />
      </section>


      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <div>
          <SectionTitle title="주요 기술 스택" desc="공고 언급 빈도 기준" />
          <Card className="p-4">
            <div className="flex flex-wrap gap-2">
              {topStacks.map(([slug, count]) => (
                <Link key={slug} href={`/stacks/${slug}`}>
                  <span className="inline-flex items-center rounded-lg bg-slate-100 px-2.5 py-1.5 text-sm font-semibold hover:bg-primary-soft hover:text-primary">
                    {STACK_NAME[slug] ?? slug}
                    <span className="ml-1.5 text-xs font-medium text-muted">{count}</span>
                  </span>
                </Link>
              ))}
              {topStacks.length === 0 ? <p className="text-sm text-muted">추출된 기술이 없습니다.</p> : null}
            </div>
          </Card>
        </div>
        <div>
          <SectionTitle title="직군 분포" />
          <Card className="divide-y divide-border">
            {company.roles.map((r) => (
              <Link key={r.slug} href={`/roles/${r.slug}`} className="flex items-center justify-between px-4 py-2.5 text-sm transition hover:bg-slate-50">
                <span className="font-semibold">{r.name}</span>
                <Badge>{r.count}건</Badge>
              </Link>
            ))}
          </Card>
        </div>
      </section>

      <section className="mt-8">
        <SectionTitle title={`${company.name} 개발 공고`} desc={`${jobs.length}건`} />
        <div className="grid gap-3 lg:grid-cols-2">
          {jobs.map((job) => <JobCard key={job.id} job={job} />)}
        </div>
      </section>
    </div>
  );
}
