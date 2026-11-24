from __future__ import annotations

import re
from dataclasses import dataclass, field

# Tech stack dictionary. Aliases are matched case-insensitively.
# Keep aliases specific: false positives are worse than missing a rare mention.
STACK_DEFS: list[dict] = [
    # Languages
    {"slug": "python", "name": "Python", "category": "언어", "aliases": ["python", "파이썬"], "blurb": "데이터·백엔드·AI 전반에서 가장 폭넓게 쓰이는 언어입니다."},
    {"slug": "java", "name": "Java", "category": "언어", "aliases": ["java", "자바"], "blurb": "대규모 백엔드와 금융·커머스 시스템에서 꾸준히 수요가 큰 언어입니다."},
    {"slug": "typescript", "name": "TypeScript", "category": "언어", "aliases": ["typescript", "타입스크립트"], "blurb": "프론트엔드와 Node.js 백엔드에서 타입 안정성을 위해 널리 사용됩니다."},
    {"slug": "javascript", "name": "JavaScript", "category": "언어", "aliases": ["javascript", "자바스크립트"], "blurb": "웹 프론트엔드의 기본 언어로, React·Vue 생태계의 기반입니다."},
    {"slug": "go", "name": "Go", "category": "언어", "aliases": ["golang", "go language", "go 개발", "go backend", "go server", "고 언어"], "blurb": "클라우드·인프라·대규모 트래픽 서비스에서 선호되는 언어입니다."},
    {"slug": "rust", "name": "Rust", "category": "언어", "aliases": ["rust", "러스트"], "blurb": "메모리 안전성과 성능이 중요한 시스템·인프라 영역에서 채택이 늘고 있습니다."},
    {"slug": "kotlin", "name": "Kotlin", "category": "언어", "aliases": ["kotlin", "코틀린"], "blurb": "안드로이드 네이티브와 서버 개발에서 함께 쓰입니다."},
    {"slug": "swift", "name": "Swift", "category": "언어", "aliases": ["swift", "스위프트"], "blurb": "iOS·macOS 앱 개발의 표준 언어입니다."},
    {"slug": "cpp", "name": "C++", "category": "언어", "aliases": ["c++", "cpp", "c플러스플러스"], "blurb": "게임 엔진·임베디드·고성능 시스템에서 사용됩니다."},
    {"slug": "csharp", "name": "C#", "category": "언어", "aliases": ["c#", "csharp", "닷넷", ".net", "asp.net"], "blurb": "게임(Unity)과 엔터프라이즈 백엔드에서 널리 쓰입니다."},
    {"slug": "php", "name": "PHP", "category": "언어", "aliases": ["php"], "blurb": "레거시 웹 서비스와 CMS 생태계에서 여전히 사용됩니다."},
    {"slug": "ruby", "name": "Ruby", "category": "언어", "aliases": ["ruby", "루비"], "blurb": "Rails 기반 스타트업 웹 서비스에서 사용됩니다."},
    {"slug": "scala", "name": "Scala", "category": "언어", "aliases": ["scala", "스칼라"], "blurb": "대규모 데이터 처리와 분산 시스템에서 사용됩니다."},

    # Frontend
    {"slug": "react", "name": "React", "category": "프론트엔드", "aliases": ["react", "react.js", "reactjs", "리액트"], "blurb": "국내 프론트엔드 공고에서 가장 자주 등장하는 UI 라이브러리입니다."},
    {"slug": "nextjs", "name": "Next.js", "category": "프론트엔드", "aliases": ["next.js", "nextjs", "넥스트.js", "넥스트js"], "blurb": "SEO와 서버 렌더링이 필요한 서비스에서 채택이 늘고 있습니다."},
    {"slug": "vue", "name": "Vue", "category": "프론트엔드", "aliases": ["vue.js", "vuejs", "vue"], "blurb": "국내 SI·커머스 프론트엔드에서 꾸준히 사용되는 프레임워크입니다."},
    {"slug": "nuxt", "name": "Nuxt", "category": "프론트엔드", "aliases": ["nuxt", "눅스트"], "blurb": "Vue 기반 풀스택 프레임워크입니다."},
    {"slug": "angular", "name": "Angular", "category": "프론트엔드", "aliases": ["angular", "앵귤러"], "blurb": "대규모 엔터프라이즈 웹 애플리케이션에서 사용됩니다."},
    {"slug": "svelte", "name": "Svelte", "category": "프론트엔드", "aliases": ["svelte", "스벨트"], "blurb": "컴파일 기반의 경량 프론트엔드 프레임워크입니다."},
    {"slug": "reactnative", "name": "React Native", "category": "모바일", "aliases": ["react native", "리액트 네이티브"], "blurb": "React로 iOS·Android 앱을 함께 개발하는 크로스플랫폼 도구입니다."},
    {"slug": "flutter", "name": "Flutter", "category": "모바일", "aliases": ["flutter", "플러터"], "blurb": "Dart 기반 크로스플랫폼 앱 프레임워크입니다."},
    {"slug": "tailwind", "name": "Tailwind CSS", "category": "프론트엔드", "aliases": ["tailwind"], "blurb": "유틸리티 클래스 기반 CSS 프레임워크입니다."},
    {"slug": "graphql", "name": "GraphQL", "category": "백엔드", "aliases": ["graphql"], "blurb": "클라이언트가 필요한 데이터를 직접 요청하는 API 쿼리 언어입니다."},
    {"slug": "grpc", "name": "gRPC", "category": "백엔드", "aliases": ["grpc"], "blurb": "마이크로서비스 간 고성능 RPC 통신에 사용됩니다."},

    # Backend
    {"slug": "nodejs", "name": "Node.js", "category": "백엔드", "aliases": ["node.js", "nodejs", "노드.js", "노드js"], "blurb": "API 서버와 풀스택 개발에서 빠르게 도입되는 런타임입니다."},
    {"slug": "spring", "name": "Spring", "category": "백엔드", "aliases": ["spring boot", "spring", "스프링"], "blurb": "국내 대기업·금융권 백엔드의 사실상 표준 프레임워크입니다."},
    {"slug": "django", "name": "Django", "category": "백엔드", "aliases": ["django", "장고"], "blurb": "Python 기반 웹 프레임워크로 빠른 제품 개발에 적합합니다."},
    {"slug": "fastapi", "name": "FastAPI", "category": "백엔드", "aliases": ["fastapi", "fast api"], "blurb": "Python 비동기 API 서버와 AI 서빙에서 채택이 늘고 있습니다."},
    {"slug": "flask", "name": "Flask", "category": "백엔드", "aliases": ["flask", "플라스크"], "blurb": "가벼운 Python 웹 서비스와 내부 도구에 사용됩니다."},
    {"slug": "nestjs", "name": "NestJS", "category": "백엔드", "aliases": ["nestjs", "nest.js"], "blurb": "TypeScript 기반의 구조화된 Node.js 프레임워크입니다."},
    {"slug": "rails", "name": "Ruby on Rails", "category": "백엔드", "aliases": ["ruby on rails", "rails", "레일즈"], "blurb": "빠른 MVP 개발로 유명한 Ruby 웹 프레임워크입니다."},
    {"slug": "laravel", "name": "Laravel", "category": "백엔드", "aliases": ["laravel", "라라벨"], "blurb": "PHP 생태계의 대표 웹 프레임워크입니다."},

    # Data / AI
    {"slug": "pytorch", "name": "PyTorch", "category": "데이터/AI", "aliases": ["pytorch", "파이토치"], "blurb": "AI 연구·프로덕션에서 가장 많이 쓰이는 딥러닝 프레임워크입니다."},
    {"slug": "tensorflow", "name": "TensorFlow", "category": "데이터/AI", "aliases": ["tensorflow", "텐서플로"], "blurb": "프로덕션 ML 파이프라인에서 꾸준히 사용됩니다."},
    {"slug": "sklearn", "name": "scikit-learn", "category": "데이터/AI", "aliases": ["scikit-learn", "sklearn", "사이킷런"], "blurb": "전통적인 머신러닝 모델링의 기본 라이브러리입니다."},
    {"slug": "pandas", "name": "pandas", "category": "데이터/AI", "aliases": ["pandas", "판다스"], "blurb": "데이터 분석·전처리의 사실상 표준 Python 라이브러리입니다."},
    {"slug": "spark", "name": "Apache Spark", "category": "데이터/AI", "aliases": ["apache spark", "spark", "스파크"], "blurb": "대규모 분산 데이터 처리에 사용됩니다."},
    {"slug": "airflow", "name": "Airflow", "category": "데이터/AI", "aliases": ["airflow", "에어플로우"], "blurb": "데이터 파이프라인 스케줄링·오케스트레이션 도구입니다."},
    {"slug": "dbt", "name": "dbt", "category": "데이터/AI", "aliases": ["dbt"], "blurb": "데이터 웨어하우스 내 변환 작업을 관리하는 도구입니다."},
    {"slug": "hadoop", "name": "Hadoop", "category": "데이터/AI", "aliases": ["hadoop", "하둡"], "blurb": "대용량 데이터 저장·처리 생태계입니다."},
    {"slug": "llm", "name": "LLM", "category": "데이터/AI", "aliases": ["llm", "llms", "large language model", "대규모 언어 모델"], "blurb": "생성형 AI 제품 개발 수요와 함께 언급이 빠르게 늘고 있습니다."},
    {"slug": "rag", "name": "RAG", "category": "데이터/AI", "aliases": ["rag", "retrieval-augmented", "retrieval augmented", "검색 증강"], "blurb": "검색과 생성형 AI를 결합한 사내 지식 서비스에서 주목받습니다."},
    {"slug": "langchain", "name": "LangChain", "category": "데이터/AI", "aliases": ["langchain", "랭체인"], "blurb": "LLM 애플리케이션 프로토타이핑에 널리 쓰이는 프레임워크입니다."},
    {"slug": "openai", "name": "OpenAI API", "category": "데이터/AI", "aliases": ["openai", "gpt-4", "gpt4", "chatgpt", "gpt api"], "blurb": "GPT API를 활용한 제품 개발 공고에서 자주 등장합니다."},
    {"slug": "anthropic", "name": "Anthropic / Claude", "category": "데이터/AI", "aliases": ["anthropic", "claude"], "blurb": "Claude API 기반 서비스와 AI 에이전트 개발에서 언급됩니다."},
    {"slug": "huggingface", "name": "Hugging Face", "category": "데이터/AI", "aliases": ["hugging face", "huggingface", "허깅페이스"], "blurb": "오픈소스 모델·데이터셋 생태계의 중심 플랫폼입니다."},
    {"slug": "vector-db", "name": "벡터 DB", "category": "데이터/AI", "aliases": ["vector database", "vector db", "벡터 db", "pinecone", "milvus", "weaviate", "qdrant", "chroma"], "blurb": "RAG와 시맨틱 검색을 위한 벡터 데이터베이스 수요입니다."},
    {"slug": "mlops", "name": "MLOps", "category": "데이터/AI", "aliases": ["mlops", "mlflow", "kubeflow"], "blurb": "모델 배포·모니터링·재학습을 운영하는 역량입니다."},
    {"slug": "prompt", "name": "프롬프트 엔지니어링", "category": "데이터/AI", "aliases": ["prompt engineering", "프롬프트 엔지니어링", "prompt engineer"], "blurb": "LLM 출력을 제품 요구에 맞게 설계하는 역량입니다."},
    {"slug": "agent", "name": "AI 에이전트", "category": "데이터/AI", "aliases": ["ai agent", "agentic", "llm agent", "ai 에이전트"], "blurb": "AI 에이전트 구축 경험이 채용 요건으로 등장하고 있습니다."},
    {"slug": "computer-vision", "name": "컴퓨터 비전", "category": "데이터/AI", "aliases": ["computer vision", "컴퓨터 비전", "object detection", "image recognition"], "blurb": "이미지·영상 인식 기반 제품에서 요구되는 역량입니다."},
    {"slug": "nlp", "name": "NLP", "category": "데이터/AI", "aliases": ["nlp", "natural language processing", "자연어 처리"], "blurb": "텍스트 이해·생성 모델을 다루는 분야입니다."},
    {"slug": "recommendation", "name": "추천 시스템", "category": "데이터/AI", "aliases": ["recommendation system", "recommender", "추천 시스템"], "blurb": "커머스·콘텐츠 서비스에서 개인화를 구현하는 역량입니다."},

    # Infra
    {"slug": "aws", "name": "AWS", "category": "인프라", "aliases": ["aws", "amazon web services"], "blurb": "국내 채용 공고에서 가장 많이 언급되는 클라우드 플랫폼입니다."},
    {"slug": "gcp", "name": "GCP", "category": "인프라", "aliases": ["gcp", "google cloud"], "blurb": "데이터·ML 워크로드에서 자주 선택되는 클라우드입니다."},
    {"slug": "azure", "name": "Azure", "category": "인프라", "aliases": ["azure", "애저"], "blurb": "엔터프라이즈 환경에서 널리 쓰이는 클라우드 플랫폼입니다."},
    {"slug": "kubernetes", "name": "Kubernetes", "category": "인프라", "aliases": ["kubernetes", "k8s", "쿠버네티스"], "blurb": "컨테이너 오케스트레이션 표준으로, DevOps·플랫폼 직군의 필수 역량입니다."},
    {"slug": "docker", "name": "Docker", "category": "인프라", "aliases": ["docker", "도커"], "blurb": "개발·배포 환경을 통일하는 기본 도구입니다."},
    {"slug": "terraform", "name": "Terraform", "category": "인프라", "aliases": ["terraform", "테라폼"], "blurb": "클라우드 인프라를 코드로 관리하는 IaC 표준입니다."},
    {"slug": "ansible", "name": "Ansible", "category": "인프라", "aliases": ["ansible", "앤서블"], "blurb": "서버 구성과 배포 자동화에 사용됩니다."},
    {"slug": "jenkins", "name": "Jenkins", "category": "인프라", "aliases": ["jenkins", "젠킨스"], "blurb": "CI/CD 파이프라인의 전통적인 표준 도구입니다."},
    {"slug": "github-actions", "name": "GitHub Actions", "category": "인프라", "aliases": ["github actions", "github action"], "blurb": "GitHub 기반 CI/CD 자동화의 기본 도구로 자리 잡았습니다."},
    {"slug": "argocd", "name": "Argo CD", "category": "인프라", "aliases": ["argo cd", "argocd"], "blurb": "Kubernetes GitOps 배포에 사용됩니다."},
    {"slug": "linux", "name": "Linux", "category": "인프라", "aliases": ["linux", "리눅스"], "blurb": "서버 운영의 기본이 되는 운영체제입니다."},
    {"slug": "nginx", "name": "Nginx", "category": "인프라", "aliases": ["nginx", "엔진엑스"], "blurb": "웹 서버·리버스 프록시로 널리 사용됩니다."},
    {"slug": "prometheus", "name": "Prometheus", "category": "인프라", "aliases": ["prometheus", "프로메테우스"], "blurb": "클라우드 네이티브 모니터링의 표준입니다."},
    {"slug": "grafana", "name": "Grafana", "category": "인프라", "aliases": ["grafana", "그라파나"], "blurb": "메트릭·로그 시각화 대시보드 도구입니다."},
    {"slug": "elasticsearch", "name": "Elasticsearch", "category": "인프라", "aliases": ["elasticsearch", "elastic search", "엘라스틱서치"], "blurb": "검색·로그 분석에 널리 쓰이는 분산 검색 엔진입니다."},
    {"slug": "opensearch", "name": "OpenSearch", "category": "인프라", "aliases": ["opensearch"], "blurb": "오픈소스 분산 검색·분석 엔진입니다."},

    # Databases / messaging
    {"slug": "kafka", "name": "Kafka", "category": "데이터베이스", "aliases": ["kafka", "카프카"], "blurb": "대용량 이벤트 스트리밍과 데이터 파이프라인의 핵심입니다."},
    {"slug": "rabbitmq", "name": "RabbitMQ", "category": "데이터베이스", "aliases": ["rabbitmq"], "blurb": "서비스 간 메시지 큐로 사용됩니다."},
    {"slug": "redis", "name": "Redis", "category": "데이터베이스", "aliases": ["redis", "레디스"], "blurb": "캐시·세션·큐 용도로 폭넓게 사용됩니다."},
    {"slug": "postgresql", "name": "PostgreSQL", "category": "데이터베이스", "aliases": ["postgresql", "postgres", "포스트그레스"], "blurb": "오픈소스 관계형 DB의 대표주자로, 스타트업에서 채택이 많습니다."},
    {"slug": "mysql", "name": "MySQL", "category": "데이터베이스", "aliases": ["mysql", "마이sql"], "blurb": "국내 웹 서비스에서 여전히 널리 쓰이는 관계형 DB입니다."},
    {"slug": "mariadb", "name": "MariaDB", "category": "데이터베이스", "aliases": ["mariadb"], "blurb": "MySQL 호환 오픈소스 관계형 DB입니다."},
    {"slug": "mongodb", "name": "MongoDB", "category": "데이터베이스", "aliases": ["mongodb", "몽고db"], "blurb": "유연한 스키마의 문서형 데이터베이스입니다."},
    {"slug": "dynamodb", "name": "DynamoDB", "category": "데이터베이스", "aliases": ["dynamodb"], "blurb": "AWS의 완전관리형 NoSQL 데이터베이스입니다."},
    {"slug": "cassandra", "name": "Cassandra", "category": "데이터베이스", "aliases": ["cassandra", "카산드라"], "blurb": "대규모 분산 쓰기 워크로드에 사용됩니다."},
    {"slug": "clickhouse", "name": "ClickHouse", "category": "데이터베이스", "aliases": ["clickhouse"], "blurb": "실시간 분석에 특화된 컬럼형 OLAP 데이터베이스입니다."},
    {"slug": "bigquery", "name": "BigQuery", "category": "데이터베이스", "aliases": ["bigquery", "big query"], "blurb": "GCP의 서버리스 데이터 웨어하우스입니다."},
    {"slug": "sqlite", "name": "SQLite", "category": "데이터베이스", "aliases": ["sqlite"], "blurb": "임베디드·로컬 환경에서 사용되는 경량 DB입니다."},

    # Game
    {"slug": "unity", "name": "Unity", "category": "게임", "aliases": ["unity", "유니티"], "blurb": "모바일·인디 게임 개발의 대표 엔진입니다."},
    {"slug": "unreal", "name": "Unreal Engine", "category": "게임", "aliases": ["unreal engine", "언리얼"], "blurb": "고사양 3D 게임 개발에 사용되는 엔진입니다."},
]


@dataclass(frozen=True)
class Stack:
    slug: str
    name: str
    category: str
    blurb: str
    patterns: tuple[re.Pattern, ...] = field(default_factory=tuple)


def _compile_alias(alias: str, slug: str) -> re.Pattern:
    escaped = re.escape(alias)
    if re.search(r"[가-힣]", alias):
        pattern = escaped
        if slug == "java" and alias == "자바":
            pattern += r"(?!스크립트)"
        if slug == "react" and alias == "리액트":
            pattern += r"(?!\s*네이티브)"
        return re.compile(pattern, re.IGNORECASE)

    flags = re.IGNORECASE
    suffix = ""

    # Context exclusions for short, ambiguous product names.
    if slug == "unity" and alias == "unity":
        suffix = r"(?!\s*catalog)"
    if slug == "spring" and alias == "spring":
        suffix = r"(?!\s+health)"
        flags = 0  # "spring" lowercase is usually a season or verb
    if slug == "react" and alias == "react":
        flags = 0  # exclude lowercase "react" (verb) and "ReAct" (prompting technique)

    return re.compile(
        rf"(?<![A-Za-z0-9]){escaped}{suffix}(?![A-Za-z0-9])",
        flags,
    )


STACKS: list[Stack] = [
    Stack(
        slug=item["slug"],
        name=item["name"],
        category=item["category"],
        blurb=item.get("blurb", ""),
        patterns=tuple(_compile_alias(alias, item["slug"]) for alias in item["aliases"]),
    )
    for item in STACK_DEFS
]

STACK_BY_SLUG: dict[str, Stack] = {stack.slug: stack for stack in STACKS}

# Vendor boards can inflate their own stack mentions.
SELF_EXCLUDE: dict[str, set[str]] = {
    "openai": {"openai"},
    "anthropic": {"anthropic"},
    "mongodb": {"mongodb"},
    "elastic": {"elasticsearch", "opensearch"},
    "gitlab": {"github-actions"},
}

AI_STACKS = {
    "pytorch",
    "tensorflow",
    "sklearn",
    "llm",
    "rag",
    "langchain",
    "openai",
    "anthropic",
    "huggingface",
    "vector-db",
    "mlops",
    "prompt",
    "agent",
    "computer-vision",
    "nlp",
    "recommendation",
}


def extract_stacks(text: str) -> list[str]:
    """Return stack slugs mentioned in the text, in dictionary order."""
    if not text:
        return []
    found: list[str] = []
    for stack in STACKS:
        for pattern in stack.patterns:
            if pattern.search(text):
                found.append(stack.slug)
                break
    return found
