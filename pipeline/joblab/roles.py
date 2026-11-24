from __future__ import annotations

import re

ROLE_META: dict[str, dict[str, str]] = {
    "backend": {
        "name": "백엔드",
        "blurb": "서버·API·데이터베이스를 설계하고 운영하는 직군입니다.",
    },
    "frontend": {
        "name": "프론트엔드",
        "blurb": "사용자 화면과 웹 인터랙션을 구현하는 직군입니다.",
    },
    "fullstack": {
        "name": "풀스택",
        "blurb": "프론트엔드와 백엔드를 함께 다루는 직군입니다.",
    },
    "ml": {
        "name": "ML / AI",
        "blurb": "모델 연구·학습·평가와 AI 제품화를 담당합니다.",
    },
    "data": {
        "name": "데이터",
        "blurb": "데이터 파이프라인과 분석 기반을 만드는 직군입니다.",
    },
    "devops": {
        "name": "DevOps / 인프라",
        "blurb": "배포·인프라·관측 가능성을 담당합니다.",
    },
    "mobile": {
        "name": "모바일",
        "blurb": "iOS·Android 앱을 개발하는 직군입니다.",
    },
    "security": {
        "name": "보안",
        "blurb": "애플리케이션과 인프라 보안을 담당합니다.",
    },
    "qa": {
        "name": "QA",
        "blurb": "테스트 자동화와 품질 보증을 담당합니다.",
    },
    "solutions": {
        "name": "솔루션 엔지니어링",
        "blurb": "고객 환경에 기술을 적용하고 문제를 해결하는 엔지니어링 직군입니다.",
    },
    "devrel": {
        "name": "개발자 관계",
        "blurb": "개발자 커뮤니티와 기술 콘텐츠를 담당합니다.",
    },
    "engineering": {
        "name": "소프트웨어 엔지니어링",
        "blurb": "직무가 세분화되지 않은 소프트웨어 개발 직군입니다.",
    },
    "business": {"name": "비개발", "blurb": ""},
    "design": {"name": "디자인", "blurb": ""},
    "pm": {"name": "PM", "blurb": ""},
    "other": {"name": "기타", "blurb": ""},
}

TECH_ROLES = {
    "backend",
    "frontend",
    "fullstack",
    "ml",
    "data",
    "devops",
    "mobile",
    "security",
    "qa",
    "solutions",
    "devrel",
    "engineering",
}


def _has(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


SOLUTIONS_PATTERNS = [
    r"developer advocate",
    r"developer evangelist",
    r"developer relations",
    r"\bdevrel\b",
    r"solutions? architect",
    r"solutions? engineer",
    r"solutions? consultant",
    r"sales engineer",
    r"pre-?sales engineer",
    r"forward deployed",
    r"\bfde\b",
    r"deployment (lead|strategist|engineer)",
    r"field engineer",
    r"technical consultant",
    r"implementation (consultant|engineer)",
    r"customer engineer",
    r"customer success engineer",
]

DEVREL_PATTERNS = [
    r"developer advocate",
    r"developer evangelist",
    r"developer relations",
    r"\bdevrel\b",
]

SECURITY_PATTERNS = [
    r"security",
    r"보안",
    r"appsec",
    r"infosec",
    r"penetration",
    r"pentest",
    r"\bsoc\b",
    r"threat",
    r"vulnerability",
    r"cyber",
    r"incident response",
    r"위협",
]

DATA_PATTERNS = [
    r"data engineer",
    r"data analyst",
    r"data architect",
    r"data pipeline",
    r"data platform",
    r"data infrastructure",
    r"data analytics",
    r"data operations",
    r"data ops",
    r"analytics engineer",
    r"business intelligence",
    r"\bbi engineer\b",
    r"database administrator",
    r"\bdba\b",
    r"\bdata\b(?!\s*cent(er|re))",
    r"데이터 엔지니어",
    r"데이터 분석",
    r"데이터 파이프라인",
]

ML_PATTERNS = [
    r"machine learning",
    r"deep learning",
    r"applied scientist",
    r"applied ai",
    r"research scientist",
    r"research engineer",
    r"data scientist",
    r"ai engineer",
    r"ai scientist",
    r"ai architect",
    r"ai research",
    r"artificial intelligence",
    r"mlops",
    r"prompt engineer",
    r"agent engineer",
    r"recommendation",
    r"genai",
    r"gen ai",
    r"\bml\b",
    r"\bllms?\b",
    r"\bnlp\b",
    r"computer vision",
    r"generative",
    r"머신러닝",
    r"딥러닝",
    r"인공지능",
    r"자연어",
    r"추천 시스템",
]

DEVOPS_PATTERNS = [
    r"devops",
    r"\bsre\b",
    r"site reliability",
    r"reliability engineer",
    r"infrastructure",
    r"platform engineer",
    r"platform operations",
    r"operations engineer",
    r"ai infra",
    r"inference platform",
    r"cloud engineer",
    r"cloud architect",
    r"kubernetes",
    r"systems? administrator",
    r"sysadmin",
    r"인프라",
]

MOBILE_PATTERNS = [
    r"android",
    r"\bios\b",
    r"mobile",
    r"flutter",
    r"react native",
    r"앱 개발",
    r"모바일",
]

QA_PATTERNS = [
    r"\bqa\b",
    r"quality assurance",
    r"test engineer",
    r"test automation",
    r"validation (analyst|engineer)",
    r"\bsdet\b",
    r"테스트",
]

FRONTEND_PATTERNS = [
    r"frontend",
    r"front-end",
    r"front end",
    r"프론트",
    r"web engineer",
    r"web developer",
    r"ui engineer",
    r"ux engineer",
    r"design engineer",
    r"react",
    r"vue",
    r"angular",
    r"svelte",
    r"next\.js",
]

BACKEND_PATTERNS = [
    r"backend",
    r"back-end",
    r"back end",
    r"server",
    r"서버",
    r"\bapi\b",
    r"spring",
    r"django",
    r"fastapi",
    r"node\.js",
    r"nestjs",
    r"rails",
    r"\bjava\b",
    r"kotlin",
    r"\bphp\b",
    r"\bruby\b",
    r"game server",
]

FULLSTACK_PATTERNS = [r"full[- ]?stack", r"풀스택"]

HARD_NON_TECH_PATTERNS = [
    # Physical / hardware role titles
    r"biomedical engineer",
    r"construction",
    r"architecture engineer",
    r"건축",
    r"facilities? engineer",
    r"hvac",
    r"civil engineer",
    r"mechanical engineer",
    r"electrical engineer",
    r"semiconductor engineer",
    r"hardware engineer",
    r"\basic\b",
    r"\bfpga\b",
    r"manufacturing engineer",
    r"industrial engineer",
    r"process engineer",
    r"equipment engineer",
    r"maintenance (engineer|technician|manager)",
    r"building engineer",
]

SOFT_NON_TECH_PATTERNS = [
    # Medical / clinical / science domains that can still be technical
    r"medical director",
    r"radiologist",
    r"pathologist",
    r"physician",
    r"nurse",
    r"pharmacist",
    r"medical affairs",
    r"clinical",
    r"regulatory affairs",
    r"biomedical",
    # Legal
    r"legal",
    r"counsel",
    r"attorney",
    r"lawyer",
    r"paralegal",
    # Finance / accounting
    r"finance",
    r"financial",
    r"accounting",
    r"\btax\b",
    r"payroll",
    r"audit",
    r"treasury",
    r"fp&a",
    # Sales / marketing / people
    r"business development",
    r"\bsales\b",
    r"marketing",
    r"마케팅",
    r"영업",
    r"세일즈",
    r"account (executive|manager|director)",
    r"\baccount(ant|ing)?\b",
    r"recruit",
    r"talent",
    r"채용",
    r"인사",
    r"\bhr\b",
    r"people (ops|operations|team)",
    r"customer success",
    r"customer service",
    r"customer support",
    r"상담",
    r"고객",
    r"partnership",
    r"파트너십",
    r"communications",
    r"커뮤니케이션",
    r"\bbrand\b",
    r"브랜드",
    r"content",
    r"콘텐츠",
    r"growth",
    r"\bcrm\b",
    r"\bgtm\b",
    r"go-to-market",
    r"revenue",
    r"strategy",
    r"전략",
    # Product / design
    r"product manager",
    r"program manager",
    r"project manager",
    r"product owner",
    r"product lead",
    r"technical product",
    r"\bpm\b",
    r"기획",
    r"designer",
    r"\bdesign\b",
    r"디자인",
    r"\bux\b",
    r"\bui\b",
    r"user research",
    # Operations / supply chain
    r"instock",
    r"supply chain",
    r"공급망",
    r"logistics",
    r"물류",
    r"fulfillment",
    r"warehouse",
    r"operations",
    r"운영",
    r"planning analyst",
    r"demand planning",
    r"category",
    r"카테고리",
    r"merchandising",
    r"머천다이징",
    r"procurement",
    r"구매",
    r"inventory",
    r"재고",
    # Physical domains that can still be technical when paired with a tech noun
    r"manufacturing",
    r"industrial",
    r"semiconductor",
    r"hardware",
    r"maintenance",
    r"building",
    r"facilities",
    r"facility",
    r"construction",
    r"mechanical",
    r"electrical",
    r"civil",
    # Security / risk functions that are not engineering
    r"risk",
    r"compliance",
    r"corporate security",
    r"physical security",
    r"loss prevention",
    r"물리보안",
    # Finance / legal / policy / support functions
    r"재무",
    r"회계",
    r"법무",
    r"transformation specialist",
    r"transformation lead",
    r"policy",
    r"정책",
    r"government",
    r"public relations",
    r"\bpr\b",
    r"office manager",
    r"executive assistant",
    r"비서",
    r"총무",
    r"chief of staff",
]

# These win even when the title contains a technical noun.
NON_TECH_OVERRIDE_PATTERNS = [
    r"developer marketing",
    r"developer program",
    r"developer advocacy",
]

# Titles containing these nouns are treated as technical even if they also
# contain a soft non-technical keyword (e.g. "Data Analyst, Growth Marketing").
TECH_NOUN_PATTERNS = [
    r"\bengineer\b",
    r"\bengineering\b",
    r"\bdeveloper\b",
    r"\barchitect\b",
    r"\bscientist\b",
    r"\banalyst\b",
    r"\badministrator\b",
    r"programmer",
    r"\bsre\b",
    r"\bswe\b",
    r"\bsde\b",
    r"\bqa\b",
    r"\bcto\b",
    r"개발자",
    r"프로그래머",
    r"엔지니어",
]

ROLE_GROUPS: list[tuple[str, list[str]]] = [
    ("ml", ML_PATTERNS),
    ("data", DATA_PATTERNS),
    ("security", SECURITY_PATTERNS),
    ("mobile", MOBILE_PATTERNS),
    ("frontend", FRONTEND_PATTERNS),
    ("backend", BACKEND_PATTERNS),
    ("fullstack", FULLSTACK_PATTERNS),
    ("devops", DEVOPS_PATTERNS),
    ("qa", QA_PATTERNS),
]

ENGINEERING_PATTERNS = [
    r"software engineer",
    r"software developer",
    r"\bengineer\b",
    r"\bdeveloper\b",
    r"개발자",
    r"프로그래머",
    r"programmer",
    r"architect",
    r"tech lead",
    r"technical lead",
    r"engineering (manager|director|lead)",
    r"(director|vp|head) of engineering",
    r"head of engineering",
    r"\bcto\b",
    r"member of technical staff",
    r"technical staff",
]

def _first_position(text: str, patterns: list[str]) -> int | None:
    positions: list[int] = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            positions.append(match.start())
    return min(positions) if positions else None


def classify_role(
    title: str,
    department: str = "",
    team: str = "",
    description: str = "",
) -> tuple[str, bool]:
    """Return (role, is_tech). Conservative: no description-only tech guesses."""
    # Leading bracket tags identify a team/division, not the role itself.
    title_l = re.sub(r"^\s*(?:\[[^\]]*\]\s*)+", "", (title or "").lower()).strip()

    if _has(title_l, DEVREL_PATTERNS):
        return "devrel", True
    if _has(title_l, SOLUTIONS_PATTERNS):
        return "solutions", True

    # Physical, medical, legal, and finance roles are never engineering,
    # even when the title contains "engineer".
    if _has(title_l, HARD_NON_TECH_PATTERNS):
        return "business", False

    if _has(title_l, NON_TECH_OVERRIDE_PATTERNS):
        return "business", False

    # Soft non-tech keywords (marketing, sales, operations, design, ...) lose
    # to an explicit technical noun such as "engineer" or "analyst".
    if _has(title_l, SOFT_NON_TECH_PATTERNS) and not _has(title_l, TECH_NOUN_PATTERNS):
        if _has(title_l, [r"designer", r"\bdesign\b", r"\bux\b", r"\bui\b", r"user research"]):
            return "design", False
        if _has(
            title_l,
            [
                r"product manager",
                r"program manager",
                r"project manager",
                r"product owner",
                r"product lead",
                r"technical product",
                r"\bpm\b",
            ],
        ):
            return "pm", False
        return "business", False

    # Pick the specialized role whose keyword appears earliest in the title.
    # This makes "Backend Engineer (Data Platform)" a backend role while
    # "Data Engineer, Backend" stays a data role.
    best_role: str | None = None
    best_pos: int | None = None
    for role, patterns in ROLE_GROUPS:
        pos = _first_position(title_l, patterns)
        if pos is None:
            continue
        if best_pos is None or pos < best_pos:
            best_role = role
            best_pos = pos
    if best_role:
        return best_role, True

    if _has(title_l, ENGINEERING_PATTERNS):
        return "engineering", True

    return "other", False


def classify_seniority(title: str) -> str:
    title_l = (title or "").lower()
    if _has(title_l, [r"\bintern\b", r"인턴"]):
        return "intern"
    if _has(
        title_l,
        [r"\bjunior\b", r"\bjr\b", r"\bentry\b", r"new grad", r"graduate", r"신입", r"0[-~]2년"],
    ):
        return "junior"
    if _has(
        title_l,
        [
            r"\blead\b",
            r"\bhead\b",
            r"director",
            r"\bvp\b",
            r"chief",
            r"\bcto\b",
            r"engineering manager",
            r"\bmanager\b",
            r"리드",
            r"팀장",
        ],
    ):
        return "lead"
    if _has(
        title_l,
        [
            r"principal",
            r"\bstaff\b",
            r"\bsenior\b",
            r"\bsr\.?\b",
            r"시니어",
            r"5년",
        ],
    ):
        return "senior"
    if _has(title_l, [r"\bmid\b", r"중급", r"3년"]):
        return "mid"
    return "unknown"


def detect_remote(
    location: str,
    workplace_type: str | None,
    is_remote: bool | None,
    description: str = "",
) -> str:
    if is_remote:
        return "remote"
    wt = (workplace_type or "").lower().replace("_", "-")
    if "remote" in wt:
        return "remote"
    if "hybrid" in wt:
        return "hybrid"
    if "on-site" in wt or "onsite" in wt:
        return "onsite"

    loc = (location or "").lower()
    if "remote" in loc:
        return "remote"
    if "hybrid" in loc:
        return "hybrid"

    desc = (description or "").lower()
    if re.search(r"(fully remote|remote work|remote-first|원격 근무|재택 근무|재택근무|풀재택)", desc):
        return "remote"
    if re.search(r"(hybrid|하이브리드|주\s*[2-3]\s*일\s*출근)", desc):
        return "hybrid"
    return "onsite"


def is_ai_role(title: str, stacks: list[str], role: str) -> bool:
    """AI-related means the role itself is AI, not merely that an AI tool is mentioned."""
    if role == "ml":
        return True
    return bool(
        re.search(
            r"(?<![a-z0-9])(ai|llm|agentic|machine learning|generative)(?![a-z0-9])",
            (title or "").lower(),
        )
    )
