# 개발자 채용 데이터랩

국내에서 채용 중인 테크 기업의 개발 공고를 매일 자동 수집해 **기술 스택 · 직군 · 기업별 채용 동향**을 분석하는 무료 웹사이트입니다.

- **라이브 사이트**: https://korean-tech-hiring.vercel.app
- **GitHub**: https://github.com/hankh-dev/korean-tech-hiring
- **수익화**: 현재는 무료로 운영 (광고 미사용)
- **유지보수**: 주 5시간 이하 목표 — GitHub Actions가 매일 데이터를 갱신하고, 푸시되면 Vercel이 자동 배포
- **스택**: Python(표준 라이브러리만) 파이프라인 → 정적 JSON → Next.js(App Router) 정적 사이트

## 구조

```
pipeline/            # Python 데이터 파이프라인 (의존성 없음)
  boards.json        # 수집 대상 ATS 보드 목록 (기업 추가는 여기에)
  editor_notes.json  # 주간 리포트 편집자 노트 (선택, 수동 작성)
  joblab/            # 수집·필터·분류·집계 모듈
  run.py             # 진입점: python3 pipeline/run.py
web/                 # Next.js 사이트
  data/              # 파이프라인이 생성하는 JSON (커밋 대상)
  app/               # 페이지 (대시보드/스택/직군/기업/공고/리포트/소개/방침)
  lib/stack-names.ts # 파이프라인이 자동 갱신하는 스택 이름 사전
.github/workflows/refresh.yml  # 매일 06:00 KST 데이터 갱신
```

## 로컬 실행

```bash
# 1) 데이터 생성 (약 1분, 네트워크 필요)
python3 pipeline/run.py            # 기본 출력: web/data

# 2) 사이트 실행
cd web
npm install
npm run dev                        # http://localhost:3000
```

데이터만 다시 굽고 싶을 때(네트워크 없이): `python3 pipeline/run.py --offline`

## 배포 (Vercel + GitHub Actions)

**라이브 사이트**: https://korean-tech-hiring.vercel.app

1. 이 저장소를 GitHub에 푸시합니다.
2. Vercel에서 저장소를 import 합니다. **Root Directory를 `web`으로** 설정하고, 빌드 명령은 기본값(`next build`)을 사용합니다.
3. `.github/workflows/refresh.yml`이 매일 `web/data`를 갱신·커밋하고, 푸시되면 Vercel이 재배포합니다. 수동 실행은 Actions 탭의 "Refresh job data" → Run workflow.
4. 안전장치: 파이프라인은 기술 공고 수가 이전 대비 50% 미만으로 떨어지면 갱신을 중단합니다(일시적 API 장애 방지). 의도된 감소라면 `--force`로 수동 실행하세요.

## 데이터 소스와 한계

- Greenhouse / Lever / Ashby / Workable의 **공개 보드 API**만 사용합니다. 이용약관상 수집이 제한된 소스(워크넷 등)는 사용하지 않습니다.
- 공고 원문은 저장·게시하지 않고, 제목·위치·기술 태그 등 메타데이터와 원문 링크만 제공합니다.
- 자체 채용 시스템을 쓰는 기업(네이버·카카오 등)은 포함되지 않습니다. 자세한 방법은 사이트의 "소개·방법론" 페이지 참고.

## 주간 리포트 편집자 노트

`pipeline/editor_notes.json`에 `"2026-W48": "이번 주 코멘트..."` 형식으로 추가하면 해당 주 리포트에 "편집자 노트" 섹션이 붙습니다. 운영 측면에서 도움이 되는 오리지널 콘텐츠이므로 주 1회 5분 정도 작성을 권장합니다.

## 커버리지 감사 (probe)와 Workday 옵트인

`scripts/probe_ats_coverage.py`는 후보 기업의 채용 페이지에서 ATS를 자동 탐지하고 한국 공고 수를 셉니다.
86곳 후보 실측 결과(2026-11): 한국 공고 보유 9곳 / 약 125건 / 개발 직군 추정 43건.

- **신규 커버리지의 대부분은 Workday**(반도체·EDA: Cadence 30, NVIDIA 19, Intel 9 등)였습니다.
- **국내 대기업·스타트업(네이버·카카오·삼성·토스·오늘의집·컬리 등)은 공개 ATS 미사용 또는 자체 시스템**이라 probe에서 한국 공고가 잡히지 않았습니다. 즉 현재 30보드 표본은 "테크·스타트업·글로벌 한국채용"에 편향되어 있으며, 이는 방법론 페이지에 공개합니다.
- **SmartRecruiters는 이 후보군에서 한국 공고 히트가 거의 없었습니다.**

### Workday를 기본 일일 파이프라인에 넣지 않는 이유

실측에서 Workday CXS API는 **IP 기반 요청 속도 제한(429)이 강합니다**(목록 POST조차 스로틀). 매일 58건+ 상세 GET을 돌리면 GitHub Actions 러너에서도 429로 실패할 수 있어, "안정적인 일일 갱신·주 5시간 이하 유지보수" 원칙과 충돌합니다. 그래서 Workday 어댑터(`fetch_workday`)는 구현해 두되 **기본 `boards.json`에는 포함하지 않습니다.**

### Workday 옵트인 활성화

감수할 수 있다면 `pipeline/boards_workday.json`(Cadence·NVIDIA, 확인된 site 경로)의 항목을 `pipeline/boards.json`에 병합하면 됩니다. 어댑터는 429 시 백오프 재시도+요청 간 지연으로 동작합니다. Intel 등 site 경로가 미확인인 테넌트는 채용 페이지에서 `/wday/cxs/{tenant}/{site}/jobs` 링크를 찾아 `site`를 채운 뒤 추가하세요.

