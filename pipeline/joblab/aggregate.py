from __future__ import annotations

from collections import Counter
from datetime import date, timedelta

from .roles import ROLE_META
from .stacks import STACK_BY_SLUG
from .text import pct, parse_date, today_kst, week_key, week_label, week_range


def _count_stacks(jobs: list[dict]) -> Counter:
    counter: Counter = Counter()
    for job in jobs:
        for slug in job.get("stacks", []):
            counter[slug] += 1
    return counter


def _stack_rows(counter: Counter, total: int) -> list[dict]:
    rows: list[dict] = []
    for slug, count in counter.most_common():
        stack = STACK_BY_SLUG.get(slug)
        if not stack:
            continue
        rows.append(
            {
                "slug": slug,
                "name": stack.name,
                "category": stack.category,
                "blurb": stack.blurb,
                "count": count,
                "share": pct(count, total),
            }
        )
    return rows


def _jobs_in_window(jobs: list[dict], start: date, end: date) -> list[dict]:
    result: list[dict] = []
    for job in jobs:
        posted = parse_date(job.get("postedAt"))
        if posted and start <= posted <= end:
            result.append(job)
    return result


def _top_stacks(jobs: list[dict], limit: int = 5) -> list[dict]:
    counter = _count_stacks(jobs)
    rows: list[dict] = []
    for slug, count in counter.most_common(limit):
        stack = STACK_BY_SLUG.get(slug)
        if stack:
            rows.append({"slug": slug, "name": stack.name, "count": count})
    return rows


def _top_roles(jobs: list[dict], limit: int = 3) -> list[dict]:
    counter = Counter(job.get("role") for job in jobs if job.get("role"))
    rows: list[dict] = []
    for role, count in counter.most_common(limit):
        meta = ROLE_META.get(role, {})
        if meta:
            rows.append({"slug": role, "name": meta.get("name", role), "count": count})
    return rows


def _top_companies(jobs: list[dict], limit: int = 5) -> list[dict]:
    counter = Counter(job.get("companySlug") for job in jobs if job.get("companySlug"))
    name_by_slug = {job["companySlug"]: job["company"] for job in jobs}
    rows: list[dict] = []
    for slug, count in counter.most_common(limit):
        rows.append({"slug": slug, "name": name_by_slug.get(slug, slug), "count": count})
    return rows


def build_stats(
    jobs: list[dict],
    boards: list[dict],
    errors: list[dict],
    all_korea_jobs: int,
    generated_at: str,
) -> dict:
    today = today_kst()
    tech_jobs = [job for job in jobs if job.get("isTech")]
    ai_jobs = [job for job in tech_jobs if job.get("isAi")]
    remote_jobs = [job for job in tech_jobs if job.get("remote") == "remote"]
    hybrid_jobs = [job for job in tech_jobs if job.get("remote") == "hybrid"]

    current_7_start = today - timedelta(days=6)
    previous_7_start = today - timedelta(days=13)
    current_30_start = today - timedelta(days=29)
    new_7 = _jobs_in_window(tech_jobs, current_7_start, today)
    new_30 = _jobs_in_window(tech_jobs, current_30_start, today)
    prev_7 = _jobs_in_window(tech_jobs, previous_7_start, current_7_start - timedelta(days=1))

    stack_counter = _count_stacks(tech_jobs)
    stack_rows = _stack_rows(stack_counter, len(tech_jobs))

    # Per-stack company examples and week-over-week movement.
    companies_by_stack: dict[str, Counter] = {}
    for job in tech_jobs:
        for slug in job.get("stacks", []):
            companies_by_stack.setdefault(slug, Counter())[job["company"]] += 1

    current_stack_counter = _count_stacks(new_7)
    previous_stack_counter = _count_stacks(prev_7)
    for row in stack_rows:
        slug = row["slug"]
        current = current_stack_counter.get(slug, 0)
        previous = previous_stack_counter.get(slug, 0)
        row["new7d"] = current
        row["delta7d"] = current - previous
        row["deltaPct"] = round((current - previous) / previous * 100) if previous else None
        row["companies"] = [
            {"name": name, "count": count}
            for name, count in companies_by_stack.get(slug, Counter()).most_common(5)
        ]

    role_counter = Counter(job["role"] for job in tech_jobs)
    role_rows: list[dict] = []
    for role, count in role_counter.most_common():
        meta = ROLE_META.get(role)
        if not meta:
            continue
        role_rows.append(
            {
                "slug": role,
                "name": meta["name"],
                "blurb": meta["blurb"],
                "count": count,
                "share": pct(count, len(tech_jobs)),
            }
        )

    seniority_counter = Counter(job.get("seniority") or "unknown" for job in tech_jobs)
    seniority_labels = {
        "intern": "인턴",
        "junior": "주니어/신입",
        "mid": "미드",
        "senior": "시니어",
        "lead": "리드/임원",
        "unknown": "직함 미표기",
    }
    seniority_rows = [
        {
            "key": key,
            "name": seniority_labels.get(key, key),
            "count": count,
            "share": pct(count, len(tech_jobs)),
        }
        for key, count in seniority_counter.most_common()
    ]

    remote_counter = Counter(job.get("remote") or "onsite" for job in tech_jobs)
    remote_labels = {"remote": "원격", "hybrid": "하이브리드", "onsite": "현장"}
    remote_rows = [
        {
            "key": key,
            "name": remote_labels.get(key, key),
            "count": count,
            "share": pct(count, len(tech_jobs)),
        }
        for key, count in remote_counter.most_common()
    ]

    company_rows: list[dict] = []
    for board in boards:
        company_jobs = [job for job in tech_jobs if job["companySlug"] == board["slug"]]
        if not company_jobs:
            continue
        company_stack_counter = _count_stacks(company_jobs)
        company_rows.append(
            {
                "slug": board["slug"],
                "name": board["name"],
                "type": board.get("type", "global"),
                "homepage": board.get("homepage", ""),
                "careers": board.get("careers", ""),
                "description": board.get("description", ""),
                "jobCount": len(company_jobs),
                "aiCount": sum(1 for job in company_jobs if job.get("isAi")),
                "remoteCount": sum(
                    1 for job in company_jobs if job.get("remote") in {"remote", "hybrid"}
                ),
                "posted7d": len(_jobs_in_window(company_jobs, current_7_start, today)),
                "latestPostedAt": max(
                    (job.get("postedAt") or "" for job in company_jobs), default=""
                ),
                "topStacks": [
                    {
                        "slug": slug,
                        "name": STACK_BY_SLUG[slug].name if slug in STACK_BY_SLUG else slug,
                        "count": count,
                    }
                    for slug, count in company_stack_counter.most_common(5)
                ],
                "roles": _top_roles(company_jobs, limit=3),
            }
        )
    company_rows.sort(key=lambda row: (-row["jobCount"], row["name"]))

    daily_new: list[dict] = []
    for offset in range(29, -1, -1):
        day = today - timedelta(days=offset)
        day_jobs = [job for job in tech_jobs if parse_date(job.get("postedAt")) == day]
        daily_new.append(
            {
                "date": day.isoformat(),
                "jobs": len(day_jobs),
                "ai": sum(1 for job in day_jobs if job.get("isAi")),
            }
        )

    weekly: list[dict] = []
    for offset in range(7, -1, -1):
        start = today - timedelta(days=today.weekday() + 7 * offset)
        end = start + timedelta(days=6)
        subset = _jobs_in_window(tech_jobs, start, end)
        weekly.append(
            {
                "week": week_key(start),
                "label": week_label(start),
                "start": start.isoformat(),
                "end": end.isoformat(),
                "partial": offset == 0,
                "jobs": len(subset),
                "aiShare": pct(sum(1 for job in subset if job.get("isAi")), len(subset)),
                "remoteShare": pct(
                    sum(1 for job in subset if job.get("remote") in {"remote", "hybrid"}),
                    len(subset),
                ),
                "topStacks": _top_stacks(subset, limit=3),
                "topRoles": _top_roles(subset, limit=2),
            }
        )

    recent_jobs = sorted(
        tech_jobs,
        key=lambda job: (job.get("postedAt") or "", job.get("company") or ""),
        reverse=True,
    )[:12]

    return {
        "generatedAt": generated_at,
        "totals": {
            "allKoreaJobs": all_korea_jobs,
            "techJobs": len(tech_jobs),
            "companies": len(company_rows),
            "aiJobs": len(ai_jobs),
            "remoteJobs": len(remote_jobs),
            "hybridJobs": len(hybrid_jobs),
            "new7d": len(new_7),
            "new30d": len(new_30),
            "stacks": len(stack_rows),
        },
        "stacks": stack_rows,
        "roles": role_rows,
        "seniority": seniority_rows,
        "remote": remote_rows,
        "companies": company_rows,
        "dailyNew": daily_new,
        "weekly": weekly,
        "recentJobs": recent_jobs,
        "meta": {
            "windowDays": 30,
            "boardCount": len(boards),
            "sources": sorted({board.get("ats") for board in boards if board.get("ats")}),
            "errors": errors,
            "note": "공개 ATS 보드에 게시된 국내 근무 공고를 기준으로 개발 직군만 집계합니다.",
        },
    }


def _report_week(
    tech_jobs: list[dict],
    start: date,
    end: date,
    note: str = "",
) -> dict | None:
    subset = _jobs_in_window(tech_jobs, start, end)
    if not subset:
        return None
    key = week_key(start)
    label = week_label(start)
    top_stacks = _top_stacks(subset, limit=5)
    top_roles = _top_roles(subset, limit=3)
    top_companies = _top_companies(subset, limit=5)
    ai_count = sum(1 for job in subset if job.get("isAi"))
    remote_count = sum(1 for job in subset if job.get("remote") in {"remote", "hybrid"})
    ai_share = pct(ai_count, len(subset))
    remote_share = pct(remote_count, len(subset))

    top_stack_text = ", ".join(f"{row['name']} {row['count']}건" for row in top_stacks) or "표본 없음"
    top_role_text = ", ".join(f"{row['name']} {row['count']}건" for row in top_roles) or "표본 없음"
    top_company_text = (
        ", ".join(f"{row['name']} {row['count']}건" for row in top_companies) or "표본 없음"
    )

    if len(subset) < 5:
        observation = "이번 주 표본이 적어 추세로 해석하기는 이릅니다. 다음 주 데이터와 함께 보는 것이 좋습니다."
    elif ai_share >= 30:
        observation = (
            "AI 관련 공고 비중이 30%를 넘었습니다. ML/AI 직군과 LLM·RAG 스택 언급이 "
            "함께 늘고 있는지 다음 주와 비교해 볼 만합니다."
        )
    elif ai_share >= 15:
        observation = "AI 관련 공고가 일정 비중을 유지하고 있습니다. 직군별로는 ML/AI와 백엔드의 경계가 흐려지는 흐름이 보입니다."
    else:
        observation = (
            "AI 관련 공고 비중은 아직 낮지만, 특정 기업의 대형 공고에 따라 변동할 수 있습니다. "
            "스택 언급은 공고 원문의 요구사항을 기준으로 집계했습니다."
        )
    if remote_share >= 30:
        observation += " 원격·하이브리드 비중이 높은 주였습니다."
    else:
        observation += " 대부분 현장 근무 공고였습니다."

    top_stack = top_stacks[0] if top_stacks else None
    top_role = top_roles[0] if top_roles else None
    summary = (
        f"{label}({start.month}/{start.day}~{end.month}/{end.day}) 국내 테크 기업의 신규 개발 공고는 "
        f"{len(subset)}건이었습니다. 가장 많이 언급된 스택은 "
        f"{top_stack['name'] if top_stack else '없음'}"
        f"({top_stack['count'] if top_stack else 0}건), 가장 많은 직군은 "
        f"{top_role['name'] if top_role else '없음'}"
        f"({top_role['count'] if top_role else 0}건)입니다."
    )

    sections = [
        {
            "heading": "이번 주 숫자",
            "body": (
                f"신규 개발 공고 {len(subset)}건, AI 관련 {ai_count}건({ai_share}%), "
                f"원격·하이브리드 {remote_count}건({remote_share}%)입니다."
            ),
        },
        {"heading": "스택 Top 5", "body": top_stack_text},
        {"heading": "직군 분포", "body": top_role_text},
        {"heading": "기업별 신규 공고", "body": top_company_text},
        {"heading": "관찰", "body": observation},
    ]
    if note:
        sections.append({"heading": "편집자 노트", "body": note})

    return {
        "slug": key.lower(),
        "week": key,
        "label": label,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "partial": end > today_kst(),
        "title": f"{label} 테크 채용 리포트",
        "summary": summary,
        "sections": sections,
        "stats": {
            "jobs": len(subset),
            "aiJobs": ai_count,
            "aiShare": ai_share,
            "remoteShare": remote_share,
            "topStacks": top_stacks,
            "topRoles": top_roles,
            "topCompanies": top_companies,
        },
    }


def build_reports(
    jobs: list[dict], notes: dict[str, str], weeks: int = 8
) -> list[dict]:
    today = today_kst()
    tech_jobs = [job for job in jobs if job.get("isTech")]
    reports: list[dict] = []
    for offset in range(weeks - 1, -1, -1):
        start = today - timedelta(days=today.weekday() + 7 * offset)
        end = start + timedelta(days=6)
        key = week_key(start)
        report = _report_week(tech_jobs, start, end, notes.get(key, ""))
        if report:
            reports.append(report)
    reports.sort(key=lambda report: report["start"], reverse=True)
    return reports


def build_history(stats: dict) -> dict:
    return {
        "date": today_kst().isoformat(),
        "allKoreaJobs": stats["totals"]["allKoreaJobs"],
        "techJobs": stats["totals"]["techJobs"],
        "aiJobs": stats["totals"]["aiJobs"],
        "companies": stats["totals"]["companies"],
        "topStacks": [
            [row["slug"], row["count"]] for row in stats["stacks"][:15]
        ],
    }
