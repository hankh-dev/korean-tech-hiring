import fs from "node:fs";
import path from "node:path";

export interface StackRow {
  slug: string;
  name: string;
  category: string;
  blurb: string;
  count: number;
  share: number;
  new7d: number;
  delta7d: number;
  deltaPct: number | null;
  companies: { name: string; count: number }[];
}

export interface RoleRow {
  slug: string;
  name: string;
  blurb: string;
  count: number;
  share: number;
}

export interface CompanyRow {
  slug: string;
  name: string;
  type: "korean" | "global";
  homepage: string;
  careers: string;
  description: string;
  jobCount: number;
  aiCount: number;
  remoteCount: number;
  posted7d: number;
  latestPostedAt: string;
  topStacks: { slug: string; name: string; count: number }[];
  roles: { slug: string; name: string; count: number }[];
}

export interface Job {
  id: string;
  company: string;
  companySlug: string;
  companyType: string;
  title: string;
  location: string;
  url: string;
  postedAt: string | null;
  employmentType: string;
  role: string;
  roleName: string;
  seniority: string;
  remote: "remote" | "hybrid" | "onsite";
  stacks: string[];
  isAi: boolean;
}

export interface WeeklyRow {
  week: string;
  label: string;
  start: string;
  end: string;
  partial: boolean;
  jobs: number;
  aiShare: number;
  remoteShare: number;
  topStacks: { slug: string; name: string; count: number }[];
  topRoles: { slug: string; name: string; count: number }[];
}

export interface Report {
  slug: string;
  week: string;
  label: string;
  start: string;
  end: string;
  partial: boolean;
  title: string;
  summary: string;
  sections: { heading: string; body: string }[];
  stats: {
    jobs: number;
    aiJobs: number;
    aiShare: number;
    remoteShare: number;
    topStacks: { slug: string; name: string; count: number }[];
    topRoles: { slug: string; name: string; count: number }[];
    topCompanies: { slug: string; name: string; count: number }[];
  };
}

export interface Stats {
  generatedAt: string;
  totals: {
    allKoreaJobs: number;
    techJobs: number;
    companies: number;
    aiJobs: number;
    remoteJobs: number;
    hybridJobs: number;
    new7d: number;
    new30d: number;
    stacks: number;
  };
  stacks: StackRow[];
  roles: RoleRow[];
  seniority: { key: string; name: string; count: number; share: number }[];
  remote: { key: string; name: string; count: number; share: number }[];
  companies: CompanyRow[];
  dailyNew: { date: string; jobs: number; ai: number }[];
  weekly: WeeklyRow[];
  recentJobs: Job[];
  meta: {
    windowDays: number;
    boardCount: number;
    sources: string[];
    errors: { board: string; error: string }[];
    note: string;
  };
}

const DATA_DIR = path.join(process.cwd(), "data");

function readJson<T>(file: string, fallback: T): T {
  try {
    return JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), "utf-8")) as T;
  } catch {
    return fallback;
  }
}

const EMPTY_STATS: Stats = {
  generatedAt: "",
  totals: {
    allKoreaJobs: 0,
    techJobs: 0,
    companies: 0,
    aiJobs: 0,
    remoteJobs: 0,
    hybridJobs: 0,
    new7d: 0,
    new30d: 0,
    stacks: 0,
  },
  stacks: [],
  roles: [],
  seniority: [],
  remote: [],
  companies: [],
  dailyNew: [],
  weekly: [],
  recentJobs: [],
  meta: { windowDays: 30, boardCount: 0, sources: [], errors: [], note: "" },
};

export function getStats(): Stats {
  return readJson<Stats>("stats.json", EMPTY_STATS);
}

export function getJobs(): Job[] {
  return readJson<{ jobs: Job[] }>("jobs.json", { jobs: [] }).jobs;
}

export function getReports(): Report[] {
  return readJson<{ reports: Report[] }>("reports.json", { reports: [] }).reports;
}

export function getStack(slug: string): StackRow | undefined {
  return getStats().stacks.find((s) => s.slug === slug);
}

export function getRole(slug: string): RoleRow | undefined {
  return getStats().roles.find((r) => r.slug === slug);
}

export function getCompany(slug: string): CompanyRow | undefined {
  return getStats().companies.find((c) => c.slug === slug);
}

export function getReport(slug: string): Report | undefined {
  return getReports().find((r) => r.slug === slug);
}

export function jobsByStack(slug: string): Job[] {
  return getJobs().filter((j) => j.stacks.includes(slug));
}

export function jobsByRole(slug: string): Job[] {
  return getJobs().filter((j) => j.role === slug);
}

export function jobsByCompany(slug: string): Job[] {
  return getJobs().filter((j) => j.companySlug === slug);
}

export {
  STACK_NAMES as STACK_NAME,
  ROLE_LABEL,
  REMOTE_LABEL,
  SENIORITY_LABEL,
  formatDate,
  formatDateTime,
  num,
} from "./labels";
