#!/usr/bin/env python3
"""Probe enterprise/public ATS coverage for Korea-based roles.

Detects which ATS a company's careers page uses (Workday, SmartRecruiters,
Greenhouse, Lever, Ashby, Workable, Recruitee, Personio, Teamtailor), then
counts Korea-based postings via each ATS's public API.

Usage: python3 scripts/probe_ats_coverage.py
Output: probe_coverage.json + printed summary.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

from joblab.roles import classify_role  # noqa: E402
from joblab.sources import is_korea  # noqa: E402

UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# (name, segment, careers url)
CANDIDATES: list[tuple[str, str, str]] = [
    # Korean portals / games / conglomerates
    ("네이버", "korean", "https://recruit.navercorp.com"),
    ("카카오", "korean", "https://careers.kakao.com"),
    ("라인", "korean", "https://careers.linecorp.com"),
    ("삼성전자", "korean", "https://www.samsung.com/sec/careers/"),
    ("LG", "korean", "https://careers.lg.com"),
    ("SK", "korean", "https://careers.sk.com"),
    ("현대자동차", "korean", "https://careers.hyundai.com"),
    ("넥슨", "korean", "https://careers.nexon.com"),
    ("엔씨소프트", "korean", "https://careers.ncsoft.com"),
    ("넷마블", "korean", "https://careers.netmarble.com"),
    ("스마일게이트", "korean", "https://careers.smilegate.com"),
    ("펄어비스", "korean", "https://www.pearlabyss.com/en-US/Careers"),
    ("네오위즈", "korean", "https://www.neowiz.com/careers"),
    ("컴투스", "korean", "https://www.com2us.com/careers"),
    ("위메이드", "korean", "https://www.wemade.com/careers"),
    # Korean startups / unicorns
    ("토스", "korean", "https://toss.im/careers"),
    ("배달의민족", "korean", "https://career.woowahan.com"),
    ("오늘의집", "korean", "https://www.bucketplace.co.kr/careers"),
    ("컬리", "korean", "https://www.kurly.com/careers"),
    ("야놀자", "korean", "https://www.yanolja.com/careers"),
    ("직방", "korean", "https://www.zigbang.com/careers"),
    ("쏘카", "korean", "https://www.socar.kr/careers"),
    ("리디", "korean", "https://www.ridi.com/careers"),
    ("매스프레소", "korean", "https://mathpresso.com/careers"),
    ("루닛(확인용)", "korean", "https://www.lunit.io/careers"),
    # Global tech with Korea offices
    ("NVIDIA", "global", "https://www.nvidia.com/en-us/about-nvidia/careers/"),
    ("Intel", "global", "https://jobs.intel.com"),
    ("AMD", "global", "https://www.amd.com/en/corporate/careers.html"),
    ("Qualcomm", "global", "https://www.qualcomm.com/company/careers"),
    ("Salesforce", "global", "https://www.salesforce.com/company/careers/"),
    ("Adobe", "global", "https://www.adobe.com/careers.html"),
    ("Netflix", "global", "https://jobs.netflix.com"),
    ("Uber", "global", "https://www.uber.com/us/en/careers/"),
    ("Tesla", "global", "https://www.tesla.com/careers"),
    ("Apple", "global", "https://www.apple.com/careers/"),
    ("Microsoft", "global", "https://careers.microsoft.com"),
    ("Google", "global", "https://www.google.com/about/careers/applications/"),
    ("Amazon", "global", "https://www.amazon.jobs"),
    ("Stripe", "global", "https://stripe.com/jobs"),
    ("Cloudflare", "global", "https://www.cloudflare.com/careers/"),
    ("Atlassian", "global", "https://www.atlassian.com/company/careers"),
    ("Shopify", "global", "https://www.shopify.com/careers"),
    ("Coinbase", "global", "https://www.coinbase.com/careers"),
    ("Roblox", "global", "https://careers.roblox.com"),
    ("Unity", "global", "https://careers.unity.com"),
    ("Epic Games", "global", "https://www.epicgames.com/site/en-US/careers"),
    ("Riot Games", "global", "https://www.riotgames.com/en/work-with-us"),
    ("EA", "global", "https://www.ea.com/careers"),
    ("Ubisoft", "global", "https://www.ubisoft.com/en-us/company/careers"),
    # Global semiconductor / equipment with Korea offices
    ("Siemens", "global", "https://www.siemens.com/global/en/company/jobs.html"),
    ("Bosch", "global", "https://www.bosch.com/careers/"),
    ("NXP", "global", "https://www.nxp.com/company/careers:Careers"),
    ("Infineon", "global", "https://www.infineon.com/cms/en/careers/"),
    ("ASML", "global", "https://www.asml.com/en/careers"),
    ("Micron", "global", "https://www.micron.com/about/careers"),
    ("Applied Materials", "global", "https://www.appliedmaterials.com/us/en/careers.html"),
    ("Lam Research", "global", "https://www.lamresearch.com/careers/"),
    ("Texas Instruments", "global", "https://www.ti.com/careers.html"),
    ("Analog Devices", "global", "https://www.analog.com/en/careers.html"),
    ("Marvell", "global", "https://www.marvell.com/company/careers.html"),
    ("Broadcom", "global", "https://www.broadcom.com/company/careers"),
    ("Synopsys", "global", "https://www.synopsys.com/careers.html"),
    ("Cadence", "global", "https://www.cadence.com/en_US/home/company/careers.html"),
    ("Arm", "global", "https://www.arm.com/company/careers"),
    ("Ericsson", "global", "https://www.ericsson.com/en/careers"),
    ("Nokia", "global", "https://www.nokia.com/about-us/careers/"),
    ("Schneider Electric", "global", "https://www.se.com/ww/en/about-us/careers/"),
    ("Honeywell", "global", "https://careers.honeywell.com"),
    ("3M", "global", "https://www.3m.com/3M/en_US/careers-us/"),
    ("Nike", "global", "https://jobs.nike.com"),
    ("Adidas", "global", "https://www.adidas-group.com/en/careers/"),
    ("Visa", "global", "https://www.visa.com/careers.html"),
    ("Mastercard", "global", "https://careers.mastercard.com"),
    ("Equinix", "global", "https://www.equinix.com/careers"),
    ("Pfizer", "global", "https://www.pfizer.com/about/careers"),
    ("Johnson & Johnson", "global", "https://jobs.jnj.com"),
    ("Roche", "global", "https://careers.roche.com"),
    ("Novartis", "global", "https://www.novartis.com/careers"),
    ("AstraZeneca", "global", "https://careers.astrazeneca.com"),
    ("GSK", "global", "https://www.gsk.com/en-gb/careers/"),
    ("Sanofi", "global", "https://www.sanofi.com/en/careers"),
    ("Bayer", "global", "https://career.bayer.com"),
    ("Merck", "global", "https://jobs.merck.com"),
    ("Eli Lilly", "global", "https://careers.lilly.com"),
    ("Moderna", "global", "https://www.modernatx.com/careers"),
    ("BioNTech", "global", "https://www.biontech.com/int/en/home/careers.html"),
]

PATTERNS = [
    ("workday", re.compile(r"https://([a-z0-9][a-z0-9-]*)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([A-Za-z0-9_\-]+)?")),
    ("smartrecruiters", re.compile(r"(?:jobs\.smartrecruiters\.com/|api\.smartrecruiters\.com/v1/companies/)([A-Za-z0-9_\-]+)")),
    ("greenhouse", re.compile(r"(?:boards\.greenhouse\.io|job-boards\.greenhouse\.io|boards-api\.greenhouse\.io/v1/boards)/([a-z0-9_\-]+)")),
    ("lever", re.compile(r"jobs\.lever\.co/([a-z0-9_\-]+)")),
    ("ashby", re.compile(r"jobs\.ashbyhq\.com/([a-z0-9_\-\.]+)")),
    ("workable", re.compile(r"(?:apply\.workable\.com/(?!api)([a-z0-9_\-]+)|https://([a-z0-9-]+)\.workable\.com)")),
    ("recruitee", re.compile(r"https://([a-z0-9-]+)\.recruitee\.com")),
    ("personio", re.compile(r"https://([a-z0-9-]+)\.jobs\.personio\.(?:de|com)")),
    ("teamtailor", re.compile(r"https://([a-z0-9-]+)\.teamtailor\.com")),
]


def http(url: str, method: str = "GET", body: dict | None = None, accept: str = "application/json"):
    headers = dict(UA)
    headers["Accept"] = accept
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode(errors="replace"))


def detect(html: str) -> tuple[str, dict] | None:
    for ats, pattern in PATTERNS:
        m = pattern.search(html)
        if not m:
            continue
        if ats == "workday":
            return ats, {"tenant": m.group(1), "shard": m.group(2), "site": m.group(3)}
        if ats == "workable":
            token = m.group(1) or m.group(2)
            if token and token not in {"apply", "www", "api"}:
                return ats, {"token": token}
            continue
        return ats, {"token": m.group(1)}
    return None


def workday_korea(cfg: dict) -> tuple[int, int, list[str]]:
    tenant, shard = cfg["tenant"], cfg["shard"]
    sites = [cfg["site"]] if cfg.get("site") else []
    sites += [
        f"{tenant.upper()}ExternalCareerSite",
        f"{tenant.capitalize()}ExternalCareerSite",
        "ExternalCareerSite",
        "External",
        f"{tenant.capitalize()}External",
        "Careers",
    ]
    for site in sites:
        if not site:
            continue
        url = f"https://{tenant}.{shard}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
        try:
            data = http(url, "POST", {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": "Korea"})
        except Exception:
            continue
        if "jobPostings" not in data:
            continue
        postings = data.get("jobPostings", [])
        total_korea = data.get("total", 0)
        try:
            seoul = http(url, "POST", {"appliedFacets": {}, "limit": 1, "offset": 0, "searchText": "Seoul"})
            total_seoul = seoul.get("total", 0)
        except Exception:
            total_seoul = 0
        tech = sum(1 for p in postings if classify_role(p.get("title", ""))[1])
        samples = [f"{p.get('title', '')} | {p.get('locationsText', '')}" for p in postings[:5]]
        return max(total_korea, total_seoul), tech, samples
    return 0, 0, []


def smartrecruiters_korea(cfg: dict) -> tuple[int, int, list[str]]:
    token = cfg["token"]
    count = 0
    tech = 0
    samples: list[str] = []
    offset = 0
    while offset < 1000:
        try:
            data = http(
                f"https://api.smartrecruiters.com/v1/companies/{token}/postings?limit=100&offset={offset}"
            )
        except Exception:
            break
        content = data.get("content") or []
        if not content:
            break
        for p in content:
            loc = p.get("location") or {}
            text = " ".join(str(loc.get(k, "")) for k in ("city", "region", "country"))
            if str(loc.get("country", "")).lower() in {"kr", "korea", "south korea"} or is_korea(text):
                count += 1
                if classify_role(p.get("title", ""))[1]:
                    tech += 1
                if len(samples) < 5:
                    samples.append(f"{p.get('title', '')} | {text}")
        offset += 100
        if offset >= data.get("totalFound", 0):
            break
    return count, tech, samples


def board_korea(ats: str, cfg: dict) -> tuple[int, int, list[str]]:
    """Lightweight Korea count for the four ATSes the pipeline already supports."""
    token = cfg["token"]
    titles: list[str] = []
    if ats == "greenhouse":
        data = http(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
        for j in data.get("jobs", []):
            loc = (j.get("location") or {}).get("name", "")
            if is_korea(loc):
                titles.append(f"{j.get('title', '')} | {loc}")
    elif ats == "lever":
        data = http(f"https://api.lever.co/v0/postings/{token}?mode=json")
        for j in data if isinstance(data, list) else []:
            cat = j.get("categories") or {}
            loc = f"{cat.get('location', '')} {j.get('country', '')}"
            if is_korea(loc):
                titles.append(f"{j.get('text', '')} | {loc}")
    elif ats == "ashby":
        data = http(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
        for j in data.get("jobs", []):
            loc = " ".join(
                str(x) for x in [j.get("location", ""), j.get("secondaryLocations", "")] if x
            )
            if is_korea(loc):
                titles.append(f"{j.get('title', '')} | {loc}")
    elif ats == "workable":
        data = http(f"https://apply.workable.com/api/v1/widget/accounts/{token}?details=true")
        for j in data.get("jobs", []):
            loc = " ".join(str(j.get(k, "")) for k in ("city", "state", "country"))
            if is_korea(loc):
                titles.append(f"{j.get('title', '')} | {loc}")
    else:
        return 0, 0, []
    tech = sum(1 for t in titles if classify_role(t.split(" | ")[0])[1])
    return len(titles), tech, titles[:5]


# Hypotheses to test when the careers page is a JS SPA / bot-blocked / wrong URL.
GUESSES: dict[str, list[tuple[str, dict]]] = {
    "NVIDIA": [("workday", {"tenant": "nvidia", "shard": "wd5", "site": "NVIDIAExternalCareerSite"})],
    "Intel": [("workday", {"tenant": "intel", "shard": "wd1", "site": None})],
    "AMD": [("workday", {"tenant": "amd", "shard": "wd1", "site": None})],
    "Qualcomm": [("workday", {"tenant": "qualcomm", "shard": "wd5", "site": None})],
    "Salesforce": [("workday", {"tenant": "salesforce", "shard": "wd12", "site": None})],
    "Adobe": [("workday", {"tenant": "adobe", "shard": "wd5", "site": None})],
    "Stripe": [("greenhouse", {"token": "stripe"})],
    "Cloudflare": [("greenhouse", {"token": "cloudflare"})],
    "루닛(확인용)": [("workable", {"token": "lunit"})],
    "토스": [("greenhouse", {"token": "toss"}), ("ashby", {"token": "toss"}), ("lever", {"token": "toss"})],
    "오늘의집": [("greenhouse", {"token": "bucketplace"}), ("ashby", {"token": "bucketplace"}), ("lever", {"token": "bucketplace"})],
    "컬리": [("greenhouse", {"token": "kurly"}), ("workable", {"token": "kurly"}), ("ashby", {"token": "kurly"})],
    "야놀자": [("greenhouse", {"token": "yanolja"}), ("lever", {"token": "yanolja"}), ("ashby", {"token": "yanolja"})],
    "직방": [("greenhouse", {"token": "zigbang"}), ("lever", {"token": "zigbang"})],
    "쏘카": [("greenhouse", {"token": "socar"}), ("lever", {"token": "socar"}), ("workable", {"token": "socar"})],
    "리디": [("greenhouse", {"token": "ridi"}), ("lever", {"token": "ridi"}), ("workable", {"token": "ridi"})],
    "매스프레소": [("greenhouse", {"token": "mathpresso"}), ("lever", {"token": "mathpresso"}), ("ashby", {"token": "mathpresso"})],
}


def _count(ats: str, cfg: dict) -> tuple[int, int, list[str]]:
    if ats == "workday":
        return workday_korea(cfg)
    if ats == "smartrecruiters":
        return smartrecruiters_korea(cfg)
    return board_korea(ats, cfg)


def probe(candidate: tuple[str, str, str]) -> dict:
    name, segment, careers = candidate
    row = {"name": name, "segment": segment, "careers": careers, "ats": None, "koreaJobs": 0, "techEst": 0, "samples": []}
    html = ""
    final_url = careers
    try:
        request = urllib.request.Request(careers, headers=UA)
        with urllib.request.urlopen(request, timeout=20) as response:
            html = response.read().decode(errors="replace")
            final_url = response.geturl()
    except Exception as exc:
        row["error"] = f"careers fetch: {exc}"
    # SPA pages embed URLs with escaped slashes; normalize before matching.
    html = html.replace("\\/", "/")
    detected = detect(html) or detect(final_url)
    options = [detected] if detected else list(GUESSES.get(name, []))
    if not options:
        row["ats"] = "in-house/unknown" if not row.get("error") else "fetch-failed"
        return row
    for ats, cfg in options:
        try:
            count, tech, samples = _count(ats, cfg)
        except Exception:
            continue
        if count > 0:
            row.update(ats=ats, config=cfg, koreaJobs=count, techEst=tech, samples=samples)
            return row
    # No Korea postings found under any hypothesis; record the first ATS tried.
    row["ats"] = options[0][0]
    row["config"] = options[0][1]
    return row


def main() -> int:
    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(probe, c): c for c in CANDIDATES}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            flag = f"{row['koreaJobs']:>4} KR" if row["koreaJobs"] else "   -"
            print(f"  {row['name']:<22} {str(row['ats']):<16} {flag}")
    rows.sort(key=lambda r: (-r["koreaJobs"], r["name"]))
    (ROOT / "probe_coverage.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    hits = [r for r in rows if r["koreaJobs"] > 0]
    print()
    print(f"후보 {len(rows)}곳 중 한국 공고 보유 {len(hits)}곳")
    print(f"한국 공고 합계(근사): {sum(r['koreaJobs'] for r in hits)}건 / 개발 직군 추정 {sum(r['techEst'] for r in hits)}건")
    for segment in ("korean", "global"):
        sub = [r for r in hits if r["segment"] == segment]
        print(f"  {segment}: {len(sub)}곳 / {sum(r['koreaJobs'] for r in sub)}건 / 개발 추정 {sum(r['techEst'] for r in sub)}건")
    print("\n상위 히트:")
    for r in hits[:25]:
        print(f"  {r['name']:<22} {r['ats']:<16} {r['koreaJobs']:>4}건 (dev~{r['techEst']})  {r.get('config', {})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
