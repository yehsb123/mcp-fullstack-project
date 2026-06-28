# AccessGuard — AI 기반 접근 권한 자동 심사 시스템

> 팀원이 접근 권한을 신청하면, AI Agent가 사내 보안 정책을 검토하고 자동 승인/반려/에스컬레이션하는 시스템

---

## 전체 아키텍처

```
사용자 (Next.js)
  │
  ▼
FastAPI 백엔드
  │
  ▼
LangGraph Agent (그래프 기반 워크플로우)
  │
  ├── [신청 접수] ─→ [정책 검색 (RAG)] ─→ [판단]
  │                                          │
  │                    ┌─────────────────────┼─────────────────────┐
  │                    ▼                     ▼                     ▼
  │              [자동 승인]           [조건부 승인]          [에스컬레이션]
  │                    │                     │                     │
  │                    ▼                     ▼                     ▼
  │              [권한 부여]           [조건 제안]            [담당자 라우팅]
  │                    │                     │                     │
  │                    └─────────────────────┼─────────────────────┘
  │                                          ▼
  │                                      [알림 발송]
  │                                          │
  │                                          ▼
  │                                      [로그 기록]
  │
  └── LangGraph Tool (MCP Tool을 래핑) ──→ MCP Server ──→ services/ ──→ PostgreSQL
        │
        │  LangGraph는 MCP를 직접 호출하지 않음.
        │  MCP Tool을 LangGraph Tool로 래핑해서 등록하면,
        │  LLM이 필요할 때 자동으로 선택해서 호출함.
        │
        ├── request_access_tool  (← MCP request_access 래핑)
        ├── check_access_tool    (← MCP check_access 래핑)
        ├── approve_access_tool  (← MCP approve_access 래핑)
        └── notify_tool          (← MCP send_notification 래핑)
```

### 호출 흐름 요약

```
1. 사용자가 Next.js 화면에서 자연어로 권한 신청
2. Next.js → FastAPI `/api/v1/agent/chat` 엔드포인트 호출 (fetch)
3. FastAPI가 LangGraph Agent 실행
4. LangGraph가 그래프 노드를 순서대로 실행:
   a. 신청 접수 노드 → MCP Tool(check_access)로 신청자 정보 조회
   b. 정책 검색 노드 → RAG(ChromaDB)에서 관련 보안 정책 검색
   c. 판단 노드 → LLM이 정책 기반으로 승인/조건부/에스컬레이션 결정
   d. 실행 노드 → MCP Tool(approve_access, send_notification) 호출
   e. 로깅 노드 → 판단 과정 전체를 audit_logs에 기록
5. MCP Server의 각 Tool이 services/ 레이어를 통해 PostgreSQL에 접근
6. 결과가 역순으로 사용자에게 반환
```

---

## 프로젝트 구조

```
mcp-fullstack-project/
│
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py             # FastAPI 엔트리포인트
│   │   ├── api/                # REST API 엔드포인트
│   │   ├── core/               # 설정, 인증
│   │   ├── db/
│   │   │   └── models/         # ORM 모델
│   │   ├── schemas/            # Pydantic 스키마
│   │   └── services/           # 비즈니스 로직
│   └── alembic/                # DB 마이그레이션
│
├── mcp-server/                 # MCP 서버
│   ├── server.py               # MCP 서버 엔트리포인트
│   └── tools/                  # MCP Tool 4개 정의
│
├── agent/                      # LangGraph Agent
│   ├── graph.py                # LangGraph 워크플로우 (노드/엣지 정의)
│   ├── nodes/                  # 각 노드 로직 (접수, 검색, 판단, 실행, 로깅)
│   ├── state.py                # Agent 상태 정의 (TypedDict)
│   └── prompts/                # 시스템 프롬프트
│
├── rag/                        # RAG 파이프라인
│   ├── docs/                   # 보안 정책 문서 (md 파일)
│   └── scripts/                # 임베딩 + 벡터DB 적재 스크립트
│
├── frontend/                   # Next.js 프론트엔드 (TypeScript)
│   ├── src/
│   │   ├── app/                # App Router 페이지
│   │   └── components/         # UI 컴포넌트
│   ├── package.json
│   └── tsconfig.json
│
├── Dockerfile                  # 앱 컨테이너 이미지
├── docker-compose.yml          # FastAPI + PostgreSQL + ChromaDB 통합
├── .env.example                # 환경변수 템플릿
├── requirements.txt            # Python 의존성
└── README.md
```

---

## 브랜치 전략

| 브랜치 | 용도 |
|--------|------|
| `main` | 배포용 (안정 버전만 머지) |
| `dev` | 개발용 (기능 구현은 여기서) |

**작업 흐름**: `dev`에서 개발 → 동작 확인 → `main`에 머지

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | FastAPI + SQLAlchemy + PostgreSQL |
| Agent | LangGraph + Claude (ChatAnthropic) |
| RAG | sentence-transformers + ChromaDB |
| MCP | MCP Python SDK |
| Frontend | Next.js (TypeScript) |
| Infra | Docker Compose |
| CI/CD | GitHub Actions + AWS EC2 |

---

## 5주 커리큘럼

> 각 주차의 핵심 원칙: **BE에서 API 만들기 → FE(Next.js)에서 fetch로 그 API 호출해서 화면 확인**
> UI는 멘토가 제공, 멘티는 API 연동(fetch) 구현에 집중
> Day 단위는 가이드라인이며, 개인 속도에 따라 유연하게 조정

### 1주차: FastAPI + DB + Next.js 기초

**목표**: API로 권한 신청 CRUD가 되고, Next.js 화면에서 신청/조회까지 동작

**Backend 체크리스트:**
- [ ] 개발 환경 세팅 (Python, Git, Docker, VS Code, Node.js)
- [ ] Docker Compose로 PostgreSQL 컨테이너 띄우기
- [ ] FastAPI 기초 (라우팅, Request/Response, Swagger UI)
- [ ] SQLAlchemy ORM 모델 설계 (users, access_requests, permissions, audit_logs)
- [ ] CRUD API 구현: `POST /api/v1/access-requests`, `GET /api/v1/access-requests`, etc.

**Frontend 체크리스트:**
- [ ] Next.js 프로젝트 세팅 (UI는 멘토가 제공)
- [ ] 권한 신청 폼 → `fetch`로 FastAPI `POST` 호출
- [ ] 신청 목록 조회 → `fetch`로 FastAPI `GET` 호출해서 표시

**산출물**: Next.js에서 권한 신청 → FastAPI → DB 저장 → 목록 조회까지 동작

---

### 2주차: MCP Server

**목표**: MCP Tool 4개가 services/ 레이어를 통해 DB에 접근하고, Next.js에서 MCP 연동 확인

**Backend 체크리스트:**
- [ ] MCP 개념 이해 (Tool, Resource, Prompt 구조)
- [ ] MCP Python SDK로 서버 기본 구조 세팅
- [ ] MCP Tool 4개 구현
  - `request_access`: 권한 신청 접수 → services/ → DB
  - `check_access`: 현재 권한 조회 → services/ → DB
  - `approve_access`: 승인/반려 처리 → services/ → DB
  - `send_notification`: 알림 발송 → services/ → DB
- [ ] MCP Tool ↔ services/ 연동 테스트

**Frontend 체크리스트:**
- [ ] 관리자용 승인/반려 처리 화면 → `fetch`로 FastAPI `PATCH` 호출 (1주차 신청자 화면과 역할 분리)
- [ ] 신청 상태 표시 (대기중/승인/반려) 실시간 반영

**산출물**: MCP Tool이 services/ 레이어를 통해 DB CRUD 동작 + Next.js 관리자 화면에서 승인/반려 처리 확인

---

### 3주차: RAG + LangGraph Agent

**목표**: LangGraph Agent가 RAG로 정책 검색 + MCP Tool 호출로 권한 심사 자동 수행

**Backend 체크리스트:**
- [ ] 보안 정책 문서 작성 (3~5개 md 파일)
- [ ] ChromaDB에 문서 임베딩 + 검색 테스트
- [ ] LangGraph 기초 (노드, 엣지, 상태, 그래프 개념)
- [ ] Agent 상태 설계 (state.py — TypedDict)
- [ ] 그래프 노드 구현:
  - 신청 접수 노드: MCP Tool(check_access)로 신청자 정보 조회
  - 정책 검색 노드: RAG(ChromaDB)에서 관련 보안 정책 검색
  - 판단 노드: LLM이 정책 기반으로 승인/조건부/에스컬레이션 결정
  - 실행 노드: MCP Tool(approve_access, send_notification) 호출
  - 로깅 노드: 판단 과정 전체를 audit_logs에 기록
- [ ] FastAPI `/api/v1/agent/chat` 엔드포인트 추가

**Frontend 체크리스트:**
- [ ] Agent 채팅 인터페이스 → `fetch`로 FastAPI `/api/v1/agent/chat` 호출
- [ ] 승인 대기 목록 화면 → `fetch`로 FastAPI API 호출
- [ ] 처리 이력 조회 화면 → `fetch`로 FastAPI API 호출

**산출물**: Next.js 채팅에서 "마케팅 대시보드 권한 주세요" → FastAPI → LangGraph Agent가 정책 검토 후 자동 처리 → 결과 화면에 표시

---

### 4주차: 통합 테스트 + 고도화 + 데모

**목표**: 전체 흐름 안정화 + Agent 판단 품질 향상 + 데모 가능 상태

**체크리스트:**
- [ ] 전체 E2E 흐름 테스트 (Next.js → FastAPI → Agent → MCP → DB → 화면)
- [ ] 엣지 케이스 처리 (잘못된 신청, 중복 신청, 권한 만료 등)
- [ ] Agent 멀티턴 대화 보완 (추가 질문, 확인 요청)
- [ ] 프롬프트 튜닝 (판단 정확도 개선)
- [ ] LangGraph 그래프 시각화 이미지 생성 (포폴용)
- [ ] 데모 시나리오 3개 준비 + 리허설
- [ ] README 정리, 코드 정리

**산출물**: 안정적으로 동작하는 데모 + 정리된 README + 그래프 시각화

---

### 5주차: Docker 배포 + CI/CD (AWS EC2)

**목표**: 전체 서비스를 Docker로 컨테이너화하고, GitHub Actions로 EC2에 자동 배포

**체크리스트:**
- [ ] AWS 계정 생성 + EC2 인스턴스 생성 (t2.micro, Ubuntu) + SSH 접속
- [ ] EC2에 Docker, Docker Compose 설치
- [ ] 보안그룹 포트 설정 (80, 443, 8000)
- [ ] Dockerfile 작성 (앱 전체 컨테이너화 — 1주차 PostgreSQL만 띄운 것과 다름)
- [ ] docker-compose.yml 완성 (FastAPI + PostgreSQL + ChromaDB 통합)
- [ ] EC2에서 docker-compose up으로 전체 서비스 실행 확인
- [ ] GitHub Actions CI 구성 (push → 린트 + 테스트)
- [ ] GitHub Actions CD 구성 (main push → EC2에 자동 배포)
- [ ] 환경변수 관리 (.env → EC2 환경변수)

**산출물**: `http://{EC2-IP}:8000` 으로 외부 접속 가능한 배포 서비스 + CI/CD 파이프라인

> **주의**: 프리티어 (t2.micro, 월 750시간 무료, 12개월). 프로젝트 종료 후 반드시 리소스 정리할 것

---

## 데모 시나리오

```
1. 신입사원 김철수가 "고객 데이터베이스 접근 권한 주세요" 신청
2. Agent가 보안 정책 검색 → "고객 DB는 Level 2, 팀장 승인 필요"
3. Agent가 팀장에게 승인 요청 알림 발송
4. 팀장이 승인 → 권한 자동 부여
5. 감사 로그에 전 과정 기록
```

---

## 사전 준비 (시작 전 설치)

### 필수 설치

| 프로그램 | 버전 | 용도 | 설치 링크 |
|---------|------|------|----------|
| **Python** | 3.11 이상 | 백엔드, Agent, MCP 전부 Python | https://www.python.org/downloads/ |
| **Git** | 최신 | 버전 관리 | https://git-scm.com/downloads |
| **Docker Desktop** | 최신 | PostgreSQL 컨테이너, 배포 | https://www.docker.com/products/docker-desktop/ |
| **Node.js** | 20 LTS | Next.js 프론트엔드 실행 | https://nodejs.org/ |
| **VS Code** | 최신 | 코드 에디터 | https://code.visualstudio.com/ |

### VS Code 추천 확장

| 확장 | 용도 |
|------|------|
| Python (Microsoft) | Python 자동완성, 린트 |
| Docker (Microsoft) | Docker 파일 지원 |
| GitLens | Git 이력 시각화 |
| REST Client 또는 Thunder Client | API 테스트 (Swagger 대안) |

### 계정 준비

| 서비스 | 필요 시점 | 비고 |
|--------|----------|------|
| **GitHub** | 1주차 | 레포 접근용 (collaborator 초대 필요) |
| **Anthropic** | 3주차 | Claude API 키 발급 (https://console.anthropic.com/) |
| **AWS** | 5주차 | EC2 배포용 — 프리티어 12개월 무료 (https://aws.amazon.com/) |

### 설치 확인 방법

터미널에서 아래 명령어가 정상 동작하면 준비 완료:

```bash
python --version    # Python 3.11.x 이상
git --version       # git version 2.x.x
docker --version    # Docker version 2x.x.x
node --version      # v20.x.x
code --version      # VS Code 버전 출력
```

---

## DB 테이블 설계

```
┌──────────────┐       ┌───────────────────┐
│    users     │       │  access_requests  │
├──────────────┤       ├───────────────────┤
│ id (PK)      │──┐    │ id (PK)           │
│ name         │  │    │ user_id (FK)      │←─┐
│ email        │  └───→│ resource_name     │  │
│ department   │       │ access_level      │  │
│ role         │       │ status            │  │
│ created_at   │       │ reason            │  │
└──────────────┘       │ created_at        │  │
                       │ updated_at        │  │
                       └───────────────────┘  │
                                              │
┌──────────────┐       ┌───────────────────┐  │
│ permissions  │       │   audit_logs      │  │
├──────────────┤       ├───────────────────┤  │
│ id (PK)      │       │ id (PK)           │  │
│ user_id (FK) │←──────│ request_id (FK)   │  │
│ resource_name│       │ action            │  │
│ access_level │       │ decision          │  │
│ granted_at   │       │ reasoning         │  │
│ expires_at   │       │ policy_referenced │  │
└──────────────┘       │ decided_by        │  │
                       │ created_at        │  │
                       └───────────────────┘  │
```

| 테이블 | 역할 | 생성 시점 |
|--------|------|----------|
| `users` | 사용자 정보 (신청자, 승인자) | 1주차 |
| `access_requests` | 권한 신청 내역 | 1주차 |
| `permissions` | 현재 부여된 권한 | 1주차 |
| `audit_logs` | Agent 판단 과정 기록 | 3주차 |

### status 값

| 값 | 의미 |
|----|------|
| `pending` | 대기중 |
| `approved` | 승인 |
| `rejected` | 반려 |
| `conditional` | 조건부 승인 |
| `escalated` | 담당자 라우팅 |

---

## API 명세

### 1주차 API

| Method | URL | 설명 |
|--------|-----|------|
| `POST` | `/api/v1/access-requests` | 권한 신청 |
| `GET` | `/api/v1/access-requests` | 신청 목록 조회 |
| `GET` | `/api/v1/access-requests/{id}` | 신청 상세 조회 |
| `PATCH` | `/api/v1/access-requests/{id}` | 신청 상태 변경 (승인/반려) |
| `GET` | `/api/v1/users/{id}/permissions` | 사용자 현재 권한 조회 |

### 3주차 API

| Method | URL | 설명 |
|--------|-----|------|
| `POST` | `/api/v1/agent/chat` | 자연어 → Agent 실행 → 결과 반환 |
| `GET` | `/api/v1/audit-logs` | 판단 이력 조회 |

---

## 환경변수 (.env)

| 변수 | 설명 | 필요 시점 |
|------|------|----------|
| `DATABASE_URL` | PostgreSQL 접속 주소 | 1주차 |
| `ANTHROPIC_API_KEY` | Claude API 키 | 3주차 |

```bash
# .env 예시
DATABASE_URL=postgresql://postgres:password@localhost:5432/accessguard
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

---

## 참고 레퍼런스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Claude API tool_use 가이드](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
