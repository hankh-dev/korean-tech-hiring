import type { Metadata } from "next";
import { getJobs } from "@/lib/data";
import { JobsExplorer } from "@/components/jobs-explorer";

export const metadata: Metadata = {
  title: "개발 채용 공고 목록",
  description: "국내 테크 기업의 개발 채용 공고를 직군·기업·기술 스택·근무형태로 검색하세요.",
};

export default function JobsPage() {
  const jobs = getJobs();
  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">개발 채용 공고</h1>
        <p className="mt-2 text-sm text-muted">
          국내 근무 기준 개발 공고 {jobs.length.toLocaleString("ko-KR")}건. 공고 제목을 누르면 원문 채용 페이지로 이동합니다.
        </p>
      </header>
      <JobsExplorer jobs={jobs} />
    </div>
  );
}
