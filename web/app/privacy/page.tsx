import type { Metadata } from "next";
import { Card, SectionTitle } from "@/components/ui";

export const metadata: Metadata = {
  title: "개인정보처리방침",
  description: "개발자 채용 데이터랩의 개인정보 처리 안내입니다.",
};

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl">
      <header className="mb-8">
        <h1 className="text-2xl font-extrabold tracking-tight sm:text-3xl">개인정보처리방침</h1>
        <p className="mt-2 text-xs text-muted">시행일: 2026년 11월 23일</p>
      </header>

      <SectionTitle title="1. 수집하는 개인정보" />
      <Card className="p-5 text-sm leading-relaxed">
        <p>
          본 사이트는 회원가입·로그인 기능이 없으며, 이용자의 이름·연락처 등 개인을 식별할 수 있는
          정보를 직접 수집하지 않습니다. 서비스 이용 과정에서 아래 정보가 자동 생성·수집될 수 있습니다.
        </p>
        <ul className="mt-3 list-disc space-y-1 pl-5 text-muted">
          <li>접속 로그, 브라우저 종류, 대략적인 지역(국가/도시 수준)</li>
        </ul>
      </Card>

      <div className="mt-6">
        <SectionTitle title="2. 채용 공고 데이터" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            사이트에 표시되는 채용 공고는 기업이 공개한 채용 보드에서 수집한 직무 정보(제목, 위치,
            기술 태그 등)입니다. 지원자 개인정보나 이력서 데이터는 수집·저장하지 않습니다.
            공고 원문의 저작권은 각 기업에 있으며, 본 사이트는 집계 통계와 원문 링크만 제공합니다.
          </p>
        </Card>
      </div>

      <div className="mt-6">
        <SectionTitle title="3. 쿠키 사용" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            본 사이트는 이용자 경험을 개선하기 위해 쿠키를 사용할 수 있습니다. 이용자는 브라우저
            설정에서 쿠키 저장을 거부할 수 있습니다.
          </p>
        </Card>
      </div>

      <div className="mt-6">
        <SectionTitle title="4. 외부 링크" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            본 사이트는 각 기업의 채용 페이지 등 외부 사이트로 링크를 제공합니다. 외부 사이트의
            개인정보 처리에 대해서는 해당 사이트의 방침이 적용되며, 본 사이트는 책임을 지지 않습니다.
          </p>
        </Card>
      </div>

      <div className="mt-6">
        <SectionTitle title="5. 문의" />
        <Card className="p-5 text-sm leading-relaxed">
          <p>
            개인정보 처리와 관련한 문의는 사이트 소개 페이지에 기재된 연락처로 접수할 수 있습니다.
            본 방침은 법령·서비스 변경에 따라 개정될 수 있으며, 개정 시 사이트를 통해 공지합니다.
          </p>
        </Card>
      </div>
    </div>
  );
}
