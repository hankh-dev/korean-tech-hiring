"use client";

import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import { JobCard } from "./job-card";
import { Badge } from "./ui";
import { ROLE_LABEL } from "@/lib/labels";
import type { Job } from "@/lib/data";

const REMOTE_OPTIONS = [
  { value: "", label: "전체 근무형태" },
  { value: "remote", label: "원격" },
  { value: "hybrid", label: "하이브리드" },
  { value: "onsite", label: "현장" },
];

export function JobsExplorer({ jobs }: { jobs: Job[] }) {
  const [query, setQuery] = useState("");
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");
  const [remote, setRemote] = useState("");
  const [aiOnly, setAiOnly] = useState(false);

  const companies = useMemo(
    () =>
      Array.from(new Map(jobs.map((j) => [j.companySlug, j.company])).entries()).sort(
        (a, b) => a[1].localeCompare(b[1], "ko")
      ),
    [jobs]
  );

  const roleCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const j of jobs) counts.set(j.role, (counts.get(j.role) ?? 0) + 1);
    return Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
  }, [jobs]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return jobs.filter((j) => {
      if (role && j.role !== role) return false;
      if (company && j.companySlug !== company) return false;
      if (remote && j.remote !== remote) return false;
      if (aiOnly && !j.isAi) return false;
      if (q) {
        const hay = `${j.title} ${j.company} ${j.location} ${j.stacks.join(" ")}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [jobs, query, role, company, remote, aiOnly]);

  const reset = () => {
    setQuery("");
    setRole("");
    setCompany("");
    setRemote("");
    setAiOnly(false);
  };

  const selectClass =
    "h-10 rounded-lg border border-border bg-card px-3 text-sm font-medium outline-none focus:border-primary";

  return (
    <div>
      <div className="rounded-2xl border border-border bg-card p-4">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="직무, 기업, 기술 스택 검색 (예: Python, 백엔드, 쿠팡)"
              className="h-10 w-full rounded-lg border border-border bg-background pl-9 pr-3 text-sm outline-none focus:border-primary"
            />
          </div>
          <div className="flex flex-wrap gap-2">
            <select value={role} onChange={(e) => setRole(e.target.value)} className={selectClass}>
              <option value="">전체 직군</option>
              {roleCounts.map(([slug, count]) => (
                <option key={slug} value={slug}>
                  {ROLE_LABEL[slug] ?? slug} ({count})
                </option>
              ))}
            </select>
            <select value={company} onChange={(e) => setCompany(e.target.value)} className={selectClass}>
              <option value="">전체 기업</option>
              {companies.map(([slug, name]) => (
                <option key={slug} value={slug}>
                  {name}
                </option>
              ))}
            </select>
            <select value={remote} onChange={(e) => setRemote(e.target.value)} className={selectClass}>
              {REMOTE_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
            <button
              onClick={() => setAiOnly((v) => !v)}
              className={`h-10 rounded-lg border px-3 text-sm font-semibold transition ${
                aiOnly
                  ? "border-violet-300 bg-violet-100 text-violet-700"
                  : "border-border bg-card text-muted hover:text-foreground"
              }`}
            >
              AI만 보기
            </button>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between text-sm">
          <p className="flex items-center gap-2 text-muted">
            <SlidersHorizontal className="h-4 w-4" />
            <span>
              <strong className="text-foreground">{filtered.length.toLocaleString("ko-KR")}</strong>
              건 표시 / 전체 {jobs.length.toLocaleString("ko-KR")}건
            </span>
          </p>
          <button onClick={reset} className="font-semibold text-primary hover:underline">
            필터 초기화
          </button>
        </div>
      </div>

      <div className="mt-4 grid gap-3">
        {filtered.length === 0 ? (
          <div className="rounded-2xl border border-border bg-card p-10 text-center text-sm text-muted">
            조건에 맞는 공고가 없습니다. 필터를 조정해 보세요.
          </div>
        ) : (
          filtered.map((job) => <JobCard key={job.id} job={job} />)
        )}
      </div>
      {filtered.length > 0 ? (
        <p className="mt-4 text-center text-xs text-muted">
          <Badge>안내</Badge> 공고 원문은 각 기업의 채용 페이지에서 확인하세요.
        </p>
      ) : null}
    </div>
  );
}
