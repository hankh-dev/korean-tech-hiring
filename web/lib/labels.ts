import { STACK_NAMES } from "./stack-names";

export { STACK_NAMES };

export const ROLE_LABEL: Record<string, string> = {
  backend: "백엔드",
  frontend: "프론트엔드",
  fullstack: "풀스택",
  ml: "ML / AI",
  data: "데이터",
  devops: "DevOps / 인프라",
  mobile: "모바일",
  security: "보안",
  qa: "QA",
  solutions: "솔루션 엔지니어링",
  devrel: "개발자 관계",
  engineering: "소프트웨어 엔지니어링",
};

export const REMOTE_LABEL: Record<string, string> = {
  remote: "원격",
  hybrid: "하이브리드",
  onsite: "현장",
};

export const SENIORITY_LABEL: Record<string, string> = {
  intern: "인턴",
  junior: "주니어",
  mid: "미드",
  senior: "시니어",
  lead: "리드",
  unknown: "",
};

export function formatDate(value: string | null): string {
  if (!value) return "";
  const [y, m, d] = value.split("-");
  return `${y}.${m}.${d}`;
}

export function formatDateTime(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  return new Intl.DateTimeFormat("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "Asia/Seoul",
  }).format(d);
}

export function num(n: number): string {
  return n.toLocaleString("ko-KR");
}
