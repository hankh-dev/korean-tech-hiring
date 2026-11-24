import Link from "next/link";
import { ArrowUpRight, MapPin } from "lucide-react";
import { Badge } from "./ui";
import {
  formatDate,
  REMOTE_LABEL,
  SENIORITY_LABEL,
  STACK_NAMES,
} from "@/lib/labels";
import type { Job } from "@/lib/data";

export function JobCard({ job }: { job: Job }) {
  const seniority = SENIORITY_LABEL[job.seniority] ?? "";
  return (
    <div className="rounded-xl border border-border bg-card p-4 transition hover:border-primary/40 hover:shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <Link
              href={`/companies/${job.companySlug}`}
              className="text-sm font-bold text-primary hover:underline"
            >
              {job.company}
            </Link>
            <Badge tone={job.companyType === "korean" ? "korean" : "global"}>
              {job.companyType === "korean" ? "국내" : "글로벌"}
            </Badge>
            {job.isAi ? <Badge tone="ai">AI</Badge> : null}
          </div>
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-1 block text-[15px] font-semibold leading-snug hover:text-primary"
          >
            {job.title}
          </a>
          <p className="mt-1 flex items-center gap-1 text-xs text-muted">
            <MapPin className="h-3 w-3" />
            {job.location}
            {job.postedAt ? <span className="ml-2">게시 {formatDate(job.postedAt)}</span> : null}
          </p>
        </div>
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          aria-label="원문 공고 보기"
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-border text-muted transition hover:border-primary hover:text-primary"
        >
          <ArrowUpRight className="h-4 w-4" />
        </a>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-1.5">
        <Link href={`/roles/${job.role}`}>
          <Badge tone="primary">{job.roleName}</Badge>
        </Link>
        <Badge tone={job.remote}>{REMOTE_LABEL[job.remote]}</Badge>
        {seniority ? <Badge>{seniority}</Badge> : null}
        {job.employmentType ? <Badge>{job.employmentType}</Badge> : null}
        {job.stacks.slice(0, 6).map((slug) => (
          <Link key={slug} href={`/stacks/${slug}`}>
            <span className="inline-flex items-center rounded-md bg-slate-100 px-1.5 py-0.5 text-[11px] font-medium text-slate-600 hover:bg-primary-soft hover:text-primary">
              {STACK_NAMES[slug] ?? slug}
            </span>
          </Link>
        ))}
        {job.stacks.length > 6 ? (
          <span className="text-[11px] text-muted">+{job.stacks.length - 6}</span>
        ) : null}
      </div>
    </div>
  );
}
