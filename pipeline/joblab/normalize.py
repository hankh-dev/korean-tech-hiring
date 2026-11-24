from __future__ import annotations

import re

from .roles import (
    ROLE_META,
    classify_role,
    classify_seniority,
    detect_remote,
    is_ai_role,
)
from .sources import RawJob
from .stacks import SELF_EXCLUDE, extract_stacks


def normalize_job(raw: RawJob) -> dict:
    text = "\n".join(
        part for part in [raw.title, raw.department, raw.team, raw.description] if part
    )
    stacks = extract_stacks(text)
    excluded = SELF_EXCLUDE.get(raw.board_slug, set())
    if excluded:
        stacks = [slug for slug in stacks if slug not in excluded]

    role, is_tech = classify_role(
        raw.title, raw.department, raw.team, raw.description
    )
    seniority = classify_seniority(raw.title)
    remote = detect_remote(
        raw.location, raw.workplace_type, raw.is_remote, raw.description
    )
    is_ai = is_ai_role(raw.title, stacks, role)

    return {
        "id": f"{raw.source}:{raw.board_slug}:{raw.source_id}",
        "source": raw.source,
        "company": raw.company_name,
        "companySlug": raw.board_slug,
        "companyType": raw.company_type,
        "title": raw.title,
        "location": raw.location,
        "url": raw.url,
        "postedAt": raw.posted_at,
        "employmentType": raw.employment_type,
        "role": role,
        "roleName": ROLE_META.get(role, {}).get("name", role),
        "isTech": is_tech,
        "seniority": seniority,
        "remote": remote,
        "stacks": stacks,
        "isAi": is_ai,
    }


def dedupe_jobs(jobs: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for job in jobs:
        by_id.setdefault(job["id"], job)

    by_key: dict[tuple[str, str, str], dict] = {}
    for job in by_id.values():
        title = re.sub(r"\s+", " ", job["title"]).strip().lower()
        key = (job["companySlug"], title, job["location"].lower())
        existing = by_key.get(key)
        if existing is None or len(job["stacks"]) > len(existing["stacks"]):
            by_key[key] = job
    return list(by_key.values())


def sort_jobs(jobs: list[dict]) -> list[dict]:
    return sorted(
        jobs,
        key=lambda job: (job.get("postedAt") or "", job.get("company") or ""),
        reverse=True,
    )
