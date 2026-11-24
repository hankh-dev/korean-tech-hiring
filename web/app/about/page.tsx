import type { Metadata } from "next";
import { getStats } from "@/lib/data";
import { Badge, Card, SectionTitle } from "@/components/ui";

export const metadata: Metadata = {
  title: "소개 · 방법론",
  description: "개발자 채용 데이터랩의 데이터 소스, 수집 방법, 분류 기준을 안내합니다.",
};

export default function AboutPage() {
  const stats = getStats();
  const sources = [
    { name: "Greenhouse", desc: "쿠팡, 당근, 크래프톤, Databricks, Anthropic 등", count: "공개 boards API" },
    { name: "Lever", desc: "채널톡, Palantir, Veeva, Gauss Labs 등", count: "공개 postings API" },
    { name: "Ashby", desc: "OpenAI, Notion, Snowflake, 무신사, BJAK 등", count: "공개 job-board API" },
    { name: "Workable", desc: "루닛 등", count: "공개 widget API" },
  ];

  return (
    <div className="max-w-3xl">
      <header className="mb-8">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">소개 · 방법론</h1>
        <p className="mt-2 text-sm text-muted">
          개발자 채용 데이터랩은 공개 채용 보드의 데이터를 자동 수집·분석해 제공하는 무료 서비스입니다.
        </p>
      </header>

      <section>
        <SectionTitle title="왜 만들었나요?" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            개발자 채용 시장은 빠르게 변하지만, 어떤 기술이 실제로 요구되는지 한눈에 보여주는 공개 데이터는
            부족했습니다. 이 사이트는 기업이 공식 채용 페이지에 게시한 공고를 기반으로, 기술 스택·직군·기업별
            채용 동향을 매일 자동 집계해 커리어 결정에 참고할 수 있는 데이터를 제공합니다.
          </p>
        </Card>
      </section>

      <section className="mt-8">
        <SectionTitle title="데이터 소스" desc={`현재 ${stats.meta.boardCount}개 채용 보드를 수집합니다`} />
        <Card className="divide-y divide-border">
          {sources.map((s) => (
            <div key={s.name} className="flex items-center justify-between gap-4 px-5 py-3">
              <div>
                <p className="text-sm font-bold">{s.name}</p>
                <p className="text-xs text-muted">{s.desc}</p>
              </div>
              <Badge>{s.count}</Badge>
            </div>
          ))}
        </Card>
        <p className="mt-3 text-xs leading-relaxed text-muted">
          기업이 자사 채용 페이지에 사용하도록 공개한 ATS(Applicant Tracking System) API만 사용합니다.
          로그인·크롤링이 필요한 비공개 데이터나 이용약관상 수집이 제한된 소스는 사용하지 않습니다.
          공고 원문은 저장·게시하지 않으며, 제목·위치·기술 태그 등 메타데이터만 집계하고 원문 링크를 제공합니다.
        </p>
      </section>

      <section className="mt-8">
        <SectionTitle title="수집·분류 방법" />
        <Card className="p-5">
          <ol className="list-decimal space-y-3 pl-5 text-sm leading-relaxed">
            <li><strong>수집:</strong> 매일 1회 각 ATS 공개 API에서 전체 공고를 가져옵니다.</li>
            <li><strong>한국 필터:</strong> 위치 필드에 한국·서울·판교·성수 등 국내 지역명이 포함된 공고만 남깁니다.</li>
            <li><strong>직군 분류:</strong> 공고 제목 기반 규칙으로 백엔드·프론트엔드·ML/AI 등 직군을 분류하고, 마케팅·영업·디자인 등 비개발 직무는 제외합니다.</li>
            <li><strong>스택 추출:</strong> 공고 제목·본문에서 사전에 정의한 기술명(별칭 포함)을 매칭합니다. Unity Catalog, Spring Health처럼 기술명이 아닌 문맥은 제외합니다.</li>
            <li><strong>집계·리포트:</strong> 스택/직군/기업별 통계와 주간 리포트를 생성해 정적 사이트로 배포합니다.</li>
          </ol>
        </Card>
      </section>

      <section className="mt-8">
        <SectionTitle title="한계와 주의사항" />
        <Card className="p-5 text-sm leading-relaxed text-muted">
          <ul className="list-disc space-y-2 pl-5">
            <li>공개 ATS를 쓰는 기업만 포함되므로, 자체 채용 시스템을 쓰는 기업(네이버·카카오 등)은 빠져 있습니다.</li>
            <li>스택 언급은 "요구 기술"의 근사치입니다. 공고에 기술명이 없으면 집계되지 않습니다.</li>
            <li>직군·시니어리티 분류는 휴리스틱이라 일부 오분류가 있을 수 있습니다.</li>
            <li>공고 게시일 기준 집계라, 실제 채용 시작·마감 시점과 다를 수 있습니다.</li>
          </ul>
        </Card>
      </section>

      <section className="mt-8">
        <SectionTitle title="운영" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            데이터는 GitHub Actions로 매일 자동 갱신되며, 사이트는 정적 페이지로 배포됩니다.
            데이터는 GitHub Actions로 매일 자동 갱신되며, 사이트는 정적 페이지로 배포됩니다.
            오류 제보나 수집 대상 기업 제안은 환영합니다.
          </p>
        </Card>
      </section>
    </div>
  );
}
