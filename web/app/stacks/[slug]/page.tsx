import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getStack, getStats, jobsByStack } from "@/lib/data";
import { Badge, Card, SectionTitle, StatCard } from "@/components/ui";
import { JobCard } from "@/components/job-card";
import { Briefcase, CalendarPlus, TrendingUp } from "lucide-react";

export function generateStaticParams() {
  return getStats().stacks.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const stack = getStack(slug);
  if (!stack) return {};
  return {
    title: `${stack.name} 채용 동향`,
    description: `${stack.name}을(를) 요구하는 국내 개발 공고 ${stack.count}건. 채용 기업과 공고 목록을 확인하세요.`,
  };
}

export default async function StackDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const stack = getStack(slug);
  if (!stack) notFound();

  const jobs = jobsByStack(slug);
  const related = getStats().stacks.filter((s) => s.category === stack.category && s.slug !== slug).slice(0, 8);

  return (
    <div>
      <nav className="mb-4 text-sm text-muted">
        <Link href="/stacks" className="hover:text-primary">스택</Link>
        <span className="mx-2">/</span>
        <span className="font-semibold text-foreground">{stack.name}</span>
      </nav>

      <header className="mb-6">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">{stack.name}</h1>
          <Badge tone="primary">{stack.category}</Badge>
        </div>
        <p className="mt-2 max-w-2xl text-sm text-muted">{stack.blurb}</p>
      </header>

      <section className="grid grid-cols-3 gap-3">
        <StatCard label="언급 공고" value={`${stack.count}`} unit="건" icon={<Briefcase className="h-4 w-4" />} hint={`전체 개발 공고의 ${stack.share}%`} />
        <StatCard label="신규 7일" value={`${stack.new7d}`} unit="건" icon={<CalendarPlus className="h-4 w-4" />} />
        <StatCard label="주간 변화" value={`${stack.delta7d > 0 ? "+" : ""}${stack.delta7d}`} unit="건" icon={<TrendingUp className="h-4 w-4" />} hint="전주 대비 신규 공고 언급" />
      </section>


      {stack.companies.length > 0 ? (
        <section className="mt-8">
          <SectionTitle title={`${stack.name}을(를) 쓰는 기업`} desc="언급 공고 수 기준" />
          <div className="flex flex-wrap gap-2">
            {stack.companies.map((c) => (
              <span key={c.name} className="rounded-xl border border-border bg-card px-3 py-2 text-sm font-semibold">
                {c.name} <span className="ml-1 text-xs font-medium text-muted">{c.count}건</span>
              </span>
            ))}
          </div>
        </section>
      ) : null}

      <section className="mt-8">
        <SectionTitle title={`${stack.name} 요구 공고`} desc={`${jobs.length}건`} />
        <div className="grid gap-3 lg:grid-cols-2">
          {jobs.map((job) => <JobCard key={job.id} job={job} />)}
        </div>
      </section>

      {related.length > 0 ? (
        <section className="mt-8">
          <SectionTitle title="같은 카테고리의 다른 기술" />
          <div className="flex flex-wrap gap-2">
            {related.map((s) => (
              <Link key={s.slug} href={`/stacks/${s.slug}`}>
                <Card className="px-3 py-2 text-sm font-semibold transition hover:border-primary/40">
                  {s.name} <span className="ml-1 text-xs text-muted">{s.count}건</span>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
