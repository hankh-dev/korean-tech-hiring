from __future__ import annotations

import json
import re
import socket
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import timedelta

from .text import flatten, strip_html, to_date

USER_AGENT = "JobLabData/0.1 (+https://github.com/; contact: hello@example.com)"
TIMEOUT = 30

KOREA_RE = re.compile(
    r"("
    r"south\s*korea|korea|seoul|busan|incheon|daegu|daejeon|gwangju|ulsan|"
    r"seongnam|pangyo|bundang|suwon|yongin|hanam|goyang|jeju|"
    r"대한민국|한국|서울|부산|인천|대구|대전|광주|울산|성남|판교|분당|수원|용인|하남|고양|제주|"
    r"강남|잠실|성수|송파|용산|마포|서초|영등포|구로|금천|성동|광진|종로|을지로|여의도|"
    r"마곡|가산|문정|상암|홍대|선릉|역삼|삼성동|중구|"
    r"경기|김포|부천|안양|과천|의왕|군포|오산|화성|평택|천안|청주|전주|창원|포항|강릉|춘천|원주|"
    r"\bKR\b"
    r")",
    re.IGNORECASE,
)


@dataclass
class RawJob:
    board_slug: str
    company_name: str
    company_type: str
    source: str
    source_id: str
    title: str
    location: str
    url: str
    description: str
    posted_at: str | None = None
    employment_type: str = ""
    workplace_type: str | None = None
    is_remote: bool | None = None
    department: str = ""
    team: str = ""


def http_json(url: str, tries: int = 3):
    last_exc: Exception | None = None
    for attempt in range(tries):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                payload = response.read().decode("utf-8")
            return json.loads(payload)
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(2 + attempt * 4)
                continue
            raise
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as exc:
            last_exc = exc
            if attempt < tries - 1:
                time.sleep(2 + attempt * 3)
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError(f"failed to fetch {url}")


def is_korea(location: str) -> bool:
    return bool(KOREA_RE.search(location or ""))


def pretty_location(location: str) -> str:
    location = re.sub(r"\s+", " ", location or "").strip(" ,|")
    if not location:
        return ""
    parts = [part.strip() for part in re.split(r"[|,]", location) if part.strip()]
    seen: set[str] = set()
    unique: list[str] = []
    for part in parts:
        key = part.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(part)
    location = ", ".join(unique)
    if not re.search(r"[가-힣]", location) and location == location.lower():
        location = location.title()
    return location


def _employment_from_metadata(metadata) -> str:
    for item in metadata or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).lower()
        if name in {"employment type", "고용형태", "고용 형태", "employment_type"}:
            return str(item.get("value", "") or "")
    return ""


def fetch_greenhouse(board: dict) -> list[RawJob]:
    token = board["token"]
    data = http_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true")
    jobs: list[RawJob] = []
    for item in data.get("jobs", []) or []:
        location = flatten(item.get("location")) or flatten(item.get("offices"))
        location = pretty_location(location)
        if not is_korea(location):
            continue
        departments = item.get("departments") or []
        department = ", ".join(str(d.get("name", "")) for d in departments if isinstance(d, dict))
        jobs.append(
            RawJob(
                board_slug=board["slug"],
                company_name=board["name"],
                company_type=board.get("type", "global"),
                source="greenhouse",
                source_id=str(item.get("id", "")),
                title=str(item.get("title", "")).strip(),
                location=location,
                url=str(item.get("absolute_url", "")),
                description=strip_html(item.get("content", "")),
                posted_at=to_date(item.get("first_published") or item.get("updated_at")),
                employment_type=_employment_from_metadata(item.get("metadata")),
                department=department,
            )
        )
    return jobs


def fetch_lever(board: dict) -> list[RawJob]:
    token = board["token"]
    data = http_json(f"https://api.lever.co/v0/postings/{token}?mode=json")
    if not isinstance(data, list):
        return []
    jobs: list[RawJob] = []
    for item in data:
        categories = item.get("categories") or {}
        location = str(categories.get("location", "") or "")
        country = str(item.get("country", "") or "")
        if country and country.lower() not in location.lower():
            location = f"{location}, {country}" if location else country
        location = pretty_location(location)
        if not is_korea(location):
            continue
        description_parts = [
            str(item.get("descriptionPlain", "") or ""),
            str(item.get("additionalPlain", "") or ""),
        ]
        for block in item.get("lists") or []:
            if isinstance(block, dict):
                description_parts.append(str(block.get("text", "") or ""))
                description_parts.append(strip_html(block.get("content", "")))
        workplace_type = item.get("workplaceType")
        jobs.append(
            RawJob(
                board_slug=board["slug"],
                company_name=board["name"],
                company_type=board.get("type", "global"),
                source="lever",
                source_id=str(item.get("id", "")),
                title=str(item.get("text", "")).strip(),
                location=location,
                url=str(item.get("hostedUrl", "")),
                description="\n".join(part for part in description_parts if part),
                posted_at=to_date(item.get("createdAt")),
                employment_type=str(categories.get("commitment", "") or ""),
                workplace_type=str(workplace_type) if workplace_type else None,
                is_remote=(str(workplace_type).lower() == "remote") if workplace_type else None,
                department=str(categories.get("department", "") or ""),
                team=str(categories.get("team", "") or ""),
            )
        )
    return jobs


def fetch_ashby(board: dict) -> list[RawJob]:
    token = board["token"]
    data = http_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
    jobs: list[RawJob] = []
    for item in data.get("jobs", []) or []:
        location = " | ".join(
            part
            for part in [
                flatten(item.get("location")),
                flatten(item.get("secondaryLocations")),
                flatten(item.get("address")),
            ]
            if part
        )
        location = pretty_location(location)
        if not is_korea(location):
            continue
        description = str(item.get("descriptionPlain", "") or "") or strip_html(
            item.get("descriptionHtml", "")
        )
        jobs.append(
            RawJob(
                board_slug=board["slug"],
                company_name=board["name"],
                company_type=board.get("type", "global"),
                source="ashby",
                source_id=str(item.get("id", "")),
                title=str(item.get("title", "")).strip(),
                location=location,
                url=str(item.get("jobUrl") or item.get("applyUrl") or ""),
                description=description,
                posted_at=to_date(item.get("publishedAt")),
                employment_type=str(item.get("employmentType", "") or ""),
                workplace_type=str(item.get("workplaceType")) if item.get("workplaceType") else None,
                is_remote=bool(item.get("isRemote")) if item.get("isRemote") is not None else None,
                department=str(item.get("department", "") or ""),
                team=str(item.get("team", "") or ""),
            )
        )
    return jobs


def fetch_workable(board: dict) -> list[RawJob]:
    token = board["token"]
    data = http_json(
        f"https://apply.workable.com/api/v1/widget/accounts/{token}?details=true"
    )
    jobs: list[RawJob] = []
    for item in data.get("jobs", []) or []:
        location = ", ".join(
            part
            for part in [
                str(item.get("city", "") or ""),
                str(item.get("state", "") or ""),
                str(item.get("country", "") or ""),
                flatten(item.get("locations")),
                str(item.get("location", "") or ""),
            ]
            if part
        )
        location = pretty_location(location)
        if not is_korea(location):
            continue
        telecommuting = bool(item.get("telecommuting"))
        jobs.append(
            RawJob(
                board_slug=board["slug"],
                company_name=board["name"],
                company_type=board.get("type", "global"),
                source="workable",
                source_id=str(item.get("shortcode") or item.get("code") or ""),
                title=str(item.get("title", "")).strip(),
                location=location,
                url=str(item.get("url") or item.get("shortlink") or ""),
                description=strip_html(item.get("description", "")),
                posted_at=to_date(item.get("published_on")),
                employment_type=str(item.get("employment_type", "") or ""),
                workplace_type="remote" if telecommuting else None,
                is_remote=telecommuting,
                department=str(item.get("department", "") or ""),
            )
        )
    return jobs


def fetch_workday(board: dict) -> list[RawJob]:
    """Workday public CXS API (opt-in; rate-limited, see README).

    Board config: {"ats": "workday", "tenant": ..., "shard": "wd1", "site": ...}
    """
    tenant = board["tenant"]
    shard = board.get("shard", "wd1")
    site = board.get("site") or "External"
    host = f"https://{tenant}.{shard}.myworkdayjobs.com"
    list_url = f"{host}/wday/cxs/{tenant}/{site}/jobs"

    seen: dict[str, dict] = {}
    for search in ("Korea", "Seoul"):
        offset = 0
        while offset < 200:
            data = http_json_post(
                list_url, {"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": search}
            )
            postings = data.get("jobPostings") or []
            if not postings:
                break
            for p in postings:
                path = p.get("externalPath", "")
                if path and is_korea(p.get("locationsText", "")):
                    seen.setdefault(path, p)
            offset += 20
            if offset >= data.get("total", 0):
                break
            time.sleep(0.4)

    jobs: list[RawJob] = []
    for path, p in seen.items():
        detail_url = f"{host}/wday/cxs/{tenant}/{site}/job/" + path.replace("/job/", "", 1)
        try:
            info = (http_json(detail_url) or {}).get("jobPostingInfo", {})
        except Exception:
            info = {}
        description = strip_html(info.get("jobDescription", ""))
        posted = to_date(info.get("startDate")) or _workday_posted_date(info.get("postedOn", ""))
        jobs.append(
            RawJob(
                board_slug=board["slug"],
                company_name=board["name"],
                company_type=board.get("type", "global"),
                source="workday",
                source_id=path.rsplit("_", 1)[-1] or path,
                title=str(info.get("title") or p.get("title", "")).strip(),
                location=pretty_location(str(info.get("location") or p.get("locationsText", ""))),
                url=f"{host}/en-US/{site}{path}",
                description=description,
                posted_at=posted,
                employment_type=str(info.get("timeType", "") or ""),
                workplace_type=str(info.get("workplaceType", "") or "") or None,
                department=str(info.get("jobFamilyGroup", "") or ""),
            )
        )
        time.sleep(0.4)
    return jobs


def _workday_posted_date(text: str) -> str | None:
    from .text import today_kst

    t = (text or "").lower()
    if "today" in t:
        return today_kst().isoformat()
    if "yesterday" in t:
        return (today_kst() - timedelta(days=1)).isoformat()
    m = re.search(r"(\d+)\+?\s*days?", t)
    if m:
        return (today_kst() - timedelta(days=int(m.group(1)))).isoformat()
    return None


def http_json_post(url: str, body: dict, tries: int = 4):
    last_exc: Exception | None = None
    for attempt in range(tries):
        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(body).encode(),
                method="POST",
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(5 + attempt * 10)
                continue
            raise
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as exc:
            last_exc = exc
            if attempt < tries - 1:
                time.sleep(3 + attempt * 3)
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError(f"failed to fetch {url}")


FETCHERS = {
    "greenhouse": fetch_greenhouse,
    "lever": fetch_lever,
    "ashby": fetch_ashby,
    "workable": fetch_workable,
    "workday": fetch_workday,
}


def fetch_board(board: dict) -> list[RawJob]:
    ats = board.get("ats")
    if ats not in FETCHERS:
        raise ValueError(f"unknown ATS: {ats}")
    return FETCHERS[ats](board)


def fetch_all(
    boards: list[dict], only: set[str] | None = None
) -> tuple[list[RawJob], list[dict]]:
    selected = [b for b in boards if not only or b["slug"] in only]
    all_jobs: list[RawJob] = []
    errors: list[dict] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_board, board): board for board in selected}
        for future in as_completed(futures):
            board = futures[future]
            try:
                jobs = future.result()
                all_jobs.extend(jobs)
                print(f"  {board['slug']:<18} {len(jobs):>3} Korea jobs")
            except Exception as exc:  # noqa: BLE001 - one board must not kill the run
                errors.append({"board": board["slug"], "error": str(exc)})
                print(f"  ! {board['slug']:<16} {exc}")
    return all_jobs, errors
