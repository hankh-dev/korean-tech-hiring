#!/usr/bin/env python3
"""Probe public ATS boards for Korea-based job postings.

Read-only research script. Not part of the production pipeline.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 12
UA = "Mozilla/5.0 (compatible; JobDataLabProbe/0.1)"

KOREA_RE = re.compile(
    r"(south\s*korea|korea|seoul|busan|incheon|daegu|daejeon|gwangju|ulsan|"
    r"seongnam|pangyo|bundang|suwon|yongin|hanam|goyang|jeju|판교|서울|부산|"
    r"인천|대구|대전|광주|울산|성남|분당|수원|용인|하남|고양|제주|\bKR\b)",
    re.IGNORECASE,
)

TOKENS = """
daangn moloco sendbird coupang musinsa zoyi gausslabs flex toss tossbank
kakaobank kakaopay kakaomobility kakaogames kakaovx naver navercloud naverz
line lineplus worksmobile woowahan baemin bucketplace ohouse zigbang kurly
yanolja class101 ridi ably banksalad channel scatterlab riiid flo coinone
dunamu upbit bithumb korbit upstage wadiz tumblbug remember wanted jumpit
programmers greeting tmony spoqa mathpresso lunit vuno standigm makinarocks
stradvision twelvelabs wrtn rutton arontier dear lablup rebellions furiosa
sapion hyperconnect hpcnt wemakeprice kakaopage kakaowebtoon kakaoenterprise
kakaomakers groundx kakaobrain ncsoft nexon netmarble krafton smilegate
pearlabyss devsisters neowiz wemade com2us gravity shifup supercat haegin
openai anthropic stripe coinbase databricks mongodb gitlab hashicorp datadog
cloudflare figma notion canva airbnb spotify palantir veeva xsolla speak
coderabbit monad.foundation bjakcareer scaleai huggingface cohere perplexity
mistral together groq cerebras sambanova snowflake confluent elastic redis
supabase vercel netlify railway render fly planetscale neon turso clerk auth0
okta twilio sendgrid mailchimp hubspot salesforce atlassian asana miro linear
retool airtable zapier n8n
""".split()


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def loc_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(str(v) for v in value.values() if isinstance(v, (str, int)))
    if isinstance(value, list):
        return " ".join(loc_text(v) for v in value)
    return str(value)


def probe_greenhouse(token: str):
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
    jobs = data.get("jobs", [])
    rows = [
        {
            "title": j.get("title", ""),
            "location": loc_text(j.get("location")),
            "url": j.get("absolute_url", ""),
            "updated": j.get("updated_at", ""),
        }
        for j in jobs
    ]
    return "greenhouse", rows


def probe_lever(token: str):
    data = get_json(f"https://api.lever.co/v0/postings/{token}?mode=json")
    rows = [
        {
            "title": j.get("text", ""),
            "location": loc_text(j.get("categories", {}).get("location")),
            "url": j.get("hostedUrl", ""),
            "updated": j.get("createdAt", ""),
        }
        for j in data
    ]
    return "lever", rows


def probe_ashby(token: str):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
    rows = []
    for j in data.get("jobs", []):
        locs = [j.get("location", "")]
        for sec in j.get("secondaryLocations", []) or []:
            locs.append(sec.get("location", "") if isinstance(sec, dict) else str(sec))
        rows.append(
            {
                "title": j.get("title", ""),
                "location": " | ".join(x for x in locs if x),
                "url": j.get("jobUrl", ""),
                "updated": j.get("publishedAt", ""),
            }
        )
    return "ashby", rows


def probe_workable(token: str):
    data = get_json(f"https://apply.workable.com/api/v1/widget/accounts/{token}?details=true")
    rows = []
    for j in data.get("jobs", []):
        loc = " ".join(
            str(x)
            for x in [
                j.get("city", ""),
                j.get("state", ""),
                j.get("country", ""),
                j.get("location", ""),
            ]
            if x
        )
        rows.append(
            {
                "title": j.get("title", ""),
                "location": loc,
                "url": j.get("url", ""),
                "updated": j.get("published_on", ""),
            }
        )
    return "workable", rows


def probe_smartrecruiters(token: str):
    data = get_json(f"https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100")
    rows = []
    for j in data.get("content", []):
        loc = j.get("location", {}) or {}
        rows.append(
            {
                "title": j.get("name", ""),
                "location": " ".join(
                    str(x) for x in [loc.get("city", ""), loc.get("country", "")] if x
                ),
                "url": f"https://jobs.smartrecruiters.com/{token}/{j.get('id', '')}",
                "updated": j.get("releasedDate", ""),
            }
        )
    return "smartrecruiters", rows


PROBES = {
    "greenhouse": probe_greenhouse,
    "lever": probe_lever,
    "ashby": probe_ashby,
    "workable": probe_workable,
    "smartrecruiters": probe_smartrecruiters,
}


def probe(token: str):
    for ats, fn in PROBES.items():
        try:
            ats_name, rows = fn(token)
            if rows:
                return token, ats_name, rows
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError):
            continue
        except Exception:
            continue
    return token, None, []


def main() -> int:
    results = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(probe, t): t for t in TOKENS}
        for fut in as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as exc:  # pragma: no cover - probe only
                print(f"ERR {futures[fut]}: {exc}", file=sys.stderr)

    hits = []
    for token, ats, rows in results:
        if not rows:
            continue
        korea = [r for r in rows if KOREA_RE.search(r["location"] or "")]
        if not korea:
            continue
        hits.append(
            {
                "token": token,
                "ats": ats,
                "total": len(rows),
                "korea": len(korea),
                "sample": korea[:5],
            }
        )

    hits.sort(key=lambda h: (-h["korea"], h["token"]))
    print(json.dumps(hits, ensure_ascii=False, indent=2))
    print(f"\n{len(hits)} boards with Korea roles", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
