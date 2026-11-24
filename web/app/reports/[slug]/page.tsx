import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getReport, getReports } from "@/lib/data";
import { Badge, Card, SectionTitle, StatCard } from "@/components/ui";
import { Briefcase, Globe2, Sparkles } from "lucide-react";

export function generateStaticParams() {
  return getReports().map((r) => ({ slug: r.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const report = getReport(slug);
  if (!report) return {};
  return { title: report.title, description: report.summary };
}

export default async function ReportDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const report = getReport(slug);
  if (!report) notFound();

  return (
    <div>
      <nav className="mb-4 text-sm text-muted">
        <Link href="/reports" className="hover:text-primary">리포트</Link>
        <span className="mx-2">/</span>
        <span className="font-semibold text-foreground">{report.label}</span>
      </nav>

      <header className="mb-6">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">{report.title}</h1>
          {report.partial ? <Badge tone="hybrid">진행 중</Badge> : null}
        </div>
        <p className="mt-2 text-xs text-muted">{report.start} ~ {report.end}</p>
        <p className="mt-3 max-w-3xl text-[15px] leading-relaxed text-muted">{report.summary}</p>
      </header>

      <section className="grid grid-cols-3 gap-3">
        <StatCard label="신규 공고" value={`${report.stats.jobs}`} unit="건" icon={<Briefcase className="h-4 w-4" />} />
        <StatCard label="AI 비중" value={`${report.stats.aiShare}`} unit="%" icon={<Sparkles className="h-4 w-4" />} hint={`${report.stats.aiJobs}건`} />
        <StatCard label="원격·하이브리드" value={`${report.stats.remoteShare}`} unit="%" icon={<Globe2 className="h-4 w-4" />} />
      </section>


      <section className="mt-8 grid gap-4 lg:grid-cols-2">
        {report.sections.map((section) => (
          <Card key={section.heading} className="p-5">
            <h2 className="text-sm font-bold text-primary">{section.heading}</h2>
            <p className="mt-2 text-sm leading-relaxed">{section.body}</p>
          </Card>
        ))}
      </section>

      <section className="mt-8">
        <SectionTitle title="이번 주 상위 기업" />
        <div className="flex flex-wrap gap-2">
          {report.stats.topCompanies.map((c) => (
            <Link key={c.slug} href={`/companies/${c.slug}`}>
              <Card className="px-3 py-2 text-sm font-semibold transition hover:border-primary/40">
                {c.name} <span className="ml-1 text-xs text-muted">{c.count}건</span>
              </Card>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
