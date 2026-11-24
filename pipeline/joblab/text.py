from __future__ import annotations

import html
import re
from datetime import date, datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    # Greenhouse returns escaped HTML; unescape before tag removal so that
    # escaped markup does not survive into the plain-text description.
    text = html.unescape(value)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</(p|li|div|h[1-6]|tr)>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def to_date(value) -> str | None:
    """Normalize common date formats to YYYY-MM-DD."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        ts = value / 1000 if value > 1_000_000_000_000 else value
        try:
            return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", text)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return None


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def today_kst() -> date:
    return datetime.now(tz=KST).date()


def now_kst() -> datetime:
    return datetime.now(tz=KST)


def week_key(day: date) -> str:
    iso = day.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def week_range(key: str) -> tuple[date, date]:
    year, week = key.split("-W")
    start = date.fromisocalendar(int(year), int(week), 1)
    return start, start + timedelta(days=6)


def week_label(start: date) -> str:
    return f"{start.year}년 {start.month}월 {((start.day - 1) // 7) + 1}주차"


def pct(part: int, total: int) -> int:
    return round(part / total * 100) if total else 0


def flatten(value) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return str(value)
