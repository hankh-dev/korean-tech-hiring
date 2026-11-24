import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getRole, getStats, jobsByRole, STACK_NAME } from "@/lib/data";
import { Badge, Card, SectionTitle } from "@/components/ui";
import { JobCard } from "@/components/job-card";

export function generateStaticParams() {
  return getStats().roles.map((r) => ({ slug: r.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const role = getRole(slug);
  if (!role) return {};
  return {
    title: `${role.name} 채용`,
    description: `국내 ${role.name} 직군 개발 공고 ${role.count}건. 요구 기술과 채용 기업을 확인하세요.`,
  };
}

export default async function RoleDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const role = getRole(slug);
  if (!role) notFound();

  const jobs = jobsByRole(slug);
  const stackCounts = new Map<string, number>();
  for (const j of jobs) for (const s of j.stacks) stackCounts.set(s, (stackCounts.get(s) ?? 0) + 1);
  const topStacks = Array.from(stackCounts.entries()).sort((a, b) => b[1] - a[1]).slice(0, 12);
  const companyCounts = new Map<string, { name: string; count: number }>();
  for (const j of jobs) {
    const cur = companyCounts.get(j.companySlug) ?? { name: j.company, count: 0 };
    cur.count += 1;
    companyCounts.set(j.companySlug, cur);
  }
  const topCompanies = Array.from(companyCounts.entries()).sort((a, b) => b[1].count - a[1].count).slice(0, 10);

  return (
    <div>
      <nav className="mb-4 text-sm text-muted">
        <Link href="/roles" className="hover:text-primary">직군</Link>
        <span className="mx-2">/</span>
        <span className="font-semibold text-foreground">{role.name}</span>
      </nav>

      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">{role.name} 채용</h1>
        <p className="mt-2 text-sm text-muted">{role.blurb} 현재 {role.count}건({role.share}%)의 공고가 열려 있습니다.</p>
      </header>


      <section className="grid gap-6 lg:grid-cols-2">
        <div>
          <SectionTitle title="이 직군에서 많이 요구하는 기술" />
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
          <SectionTitle title="채용 기업" />
          <Card className="divide-y divide-border">
            {topCompanies.map(([slug, c]) => (
              <Link key={slug} href={`/companies/${slug}`} className="flex items-center justify-between px-4 py-2.5 text-sm transition hover:bg-slate-50">
                <span className="font-semibold">{c.name}</span>
                <Badge>{c.count}건</Badge>
              </Link>
            ))}
          </Card>
        </div>
      </section>

      <section className="mt-8">
        <SectionTitle title={`${role.name} 공고 목록`} desc={`${jobs.length}건`} />
        <div className="grid gap-3 lg:grid-cols-2">
          {jobs.map((job) => <JobCard key={job.id} job={job} />)}
        </div>
      </section>
    </div>
  );
}
