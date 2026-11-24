#!/usr/bin/env python3
"""Discover NEW public-ATS boards with Korea roles that we don't collect yet.

Re-runs the coverage probe over the watchlist, diffs hits against
pipeline/boards.json, and emits ready-to-paste board entries + a markdown
issue body. Used by .github/workflows/discover.yml (quarterly).

Usage: python3 scripts/discover_boards.py
Outputs: suggestions.md, suggestions.count, pipeline/board_suggestions.json
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from probe_ats_coverage import CANDIDATES, probe  # noqa: E402


def board_key(ats: str, cfg: dict) -> tuple:
    if ats == "workday":
        return ("workday", cfg.get("tenant"))
    return (ats, cfg.get("token"))


def to_entry(row: dict) -> dict:
    cfg = row.get("config") or {}
    entry = {
        "slug": cfg.get("token") or cfg.get("tenant"),
        "name": row["name"],
        "type": row["segment"],
        "ats": row["ats"],
        "homepage": "",
        "careers": row["careers"],
        "description": "",
    }
    if row["ats"] == "workday":
        entry.update(tenant=cfg.get("tenant"), shard=cfg.get("shard"), site=cfg.get("site") or "")
    else:
        entry["token"] = cfg.get("token")
    return entry


def main() -> int:
    boards = json.loads((ROOT / "pipeline" / "boards.json").read_text(encoding="utf-8"))
    existing = {board_key(b["ats"], b) for b in boards}

    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(probe, c): c for c in CANDIDATES}
        for future in as_completed(futures):
            rows.append(future.result())

    hits = [r for r in rows if r["koreaJobs"] > 0]
    new = []
    for r in hits:
        if board_key(r["ats"], r.get("config") or {}) in existing:
            continue
        new.append(r)
    new.sort(key=lambda r: -r["koreaJobs"])

    standard = [r for r in new if r["ats"] != "workday"]
    workday = [r for r in new if r["ats"] == "workday"]

    (ROOT / "pipeline" / "board_suggestions.json").write_text(
        json.dumps(
            {"standard": [to_entry(r) for r in standard], "workday": [to_entry(r) for r in workday], "raw": new},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "suggestions.count").write_text(str(len(new)) + "\n", encoding="utf-8")

    lines = [
        f"## 신규 ATS 채택 후보 {len(new)}곳 (분기 자동 probe)",
        "",
        f"watchlist {len(CANDIDATES)}곳 실측 결과, 한국 공고를 보유하지만 아직 수집하지 않는 보드입니다.",
        f"(한국 공고 보유 전체 {len(hits)}곳 중 기존 수집 제외)",
        "",
    ]
    if standard:
        lines += ["### 바로 추가 가능 (Greenhouse/Lever/Ashby/Workable/SmartRecruiters)", "",
                  "| 기업 | ATS | 한국 공고 | 개발 추정 |", "|---|---|---|---|"]
        for r in standard:
            lines.append(f"| {r['name']} | {r['ats']} | {r['koreaJobs']} | ~{r['techEst']} |")
        lines += ["", "`pipeline/boards.json`에 붙여넣을 항목:", "", "```json",
                  json.dumps([to_entry(r) for r in standard], ensure_ascii=False, indent=2), "```", ""]
    if workday:
        lines += ["### Workday (옵트인 권장 — 요청 속도 제한 강함, README 참고)", "",
                  "| 기업 | tenant/shard/site | 한국 공고 | 개발 추정 |", "|---|---|---|---|"]
        for r in workday:
            c = r.get("config") or {}
            lines.append(f"| {r['name']} | {c.get('tenant')}/{c.get('shard')}/{c.get('site')} | {r['koreaJobs']} | ~{r['techEst']} |")
        lines += ["", "`pipeline/boards_workday.json` 후보:", "", "```json",
                  json.dumps([to_entry(r) for r in workday], ensure_ascii=False, indent=2), "```", ""]
    if not new:
        lines += ["신규 후보 없음. 현재 커버리지 유지.", ""]
    lines += ["---", "_자동 생성: scripts/discover_boards.py (probe: scripts/probe_ats_coverage.py). 숫자는 근사/하한입니다._"]

    (ROOT / "suggestions.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"hits={len(hits)} new={len(new)} (standard={len(standard)}, workday={len(workday)})")
    for r in new:
        print(f"  NEW {r['name']:<20} {r['ats']:<16} {r['koreaJobs']:>4} KR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
