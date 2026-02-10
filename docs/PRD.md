# [PRD] 개인화된 AI 보안 시나리오 생성 및 훈련 플랫폼 (MVP)

## 1. 프로젝트 개요

* **프로젝트명:** Security Vibe (가칭)
* **목표:** 최신 보안 이슈 검색(Google Search)과 사용자 취향을 반영한 개인화 피싱 시나리오를 생성하고, 이메일 모의 훈련을 통해 사용자의 보안 인식을 제고하는 플랫폼.
* **배포 환경:** **Streamlit Cloud** (무료, GitHub 연동 배포)
* **핵심 로직:**
1. 사용자 이메일 로그인 (식별자 역할)
2. Gemini + Google Search로 최신 위협 정보 수집
3. SMTP를 통한 모의 해킹 메일 발송
4. 사용자가 메일 내 링크 클릭 시, 이를 감지하여 위협 분석 리포트 제공



## 2. 사용자 시나리오 (User Flow)

1. **접속 및 로그인:** 웹페이지 접속 -> 이메일 주소 입력 (간편 로그인).
2. **메인 대시보드:**
* 나의 훈련 이력 확인.
* 최신 보안 뉴스 피드 확인.
* (링크 클릭 이력이 있을 경우) 내가 취약한 위협 패턴 분석 보고서 확인.


3. **훈련 설정 (사이드바):**
* 관심사(쇼핑, 금융 등) 선택.
* 사용할 LLM 모델 및 API Key 설정.


4. **시나리오 생성 및 발송:**
* "공격 시뮬레이션 시작" 버튼 클릭.
* 시스템이 시나리오 생성 후 사용자 메일로 발송.


5. **피드백 (함정 클릭 시):**
* 사용자가 메일함에서 링크 클릭.
* 경고 페이지로 리다이렉트 되며, 대시보드의 '취약 패턴 분석' 데이터가 업데이트됨.



## 3. 상세 기능 명세

### 3.1. 메인 페이지 (Dashboard UI)

* **헤더:** 사용자 환영 메시지 (e.g., "{이메일}님의 보안 레벨: 위험 🚨")
* **섹션 1: 최신 보안 브리핑 (News Feed)**
* **기능:** Gemini에 `tools='google_search'`를 적용하여 "오늘의 대한민국 사이버 보안 이슈 Top 3"를 요약해서 출력.


* **섹션 2: 나의 훈련 로그 (History)**
* **표시:** 생성일시, 선택한 관심사, 시나리오 제목, 상태(발송됨/클릭함).


* **섹션 3: 위협 분석 리포트 (Vulnerability Report)**
* **조건:** 사용자가 피싱 메일의 링크를 클릭하고 돌아왔을 때만 활성화/업데이트.
* **내용:** "당신은 '택배 사칭' 유형에 약합니다. URL의 도메인을 확인하는 습관이 필요합니다." (LLM이 클릭된 시나리오를 분석하여 생성).



### 3.2. 시나리오 생성 및 발송 (Core Logic)

* **입력 (Sidebar):**
* API Key (OpenAI/Gemini/Claude)
* 관심사 태그 (여행, 쇼핑, 공공기관, 사내공지 등)
* Sender Email info (SMTP용 아이디/앱 비밀번호)


* **프로세스:**
1. **Search:** 선택한 관심사와 관련된 최신 해킹 사례 검색 (Gemini Grounding).
2. **Generate:** 검색된 사례를 기반으로 피해자 맞춤형 이메일 본문 생성.
3. **Send:** Python `smtplib` 활용.
* **중요:** 이메일 본문의 링크는 `https://[배포된앱주소]/?clicked=true&scenario_type=[유형]` 형태로 구성하여 클릭 여부를 추적 가능하게 함.





### 3.3. 링크 클릭 감지 및 교육 페이지

* **작동 원리:** `st.query_params` (Streamlit 기능)를 사용하여 URL 파라미터 감지.
* **화면:**
* 파라미터에 `clicked=true`가 있으면 메인 화면 진입 전 **"🚨 모의 훈련 경고창"**을 먼저 띄움.
* "이것은 모의 훈련이었습니다. 방금 클릭한 링크의 위험 요소는 다음과 같습니다..." 출력.
* "대시보드로 돌아가기" 버튼 클릭 시, 메인 대시보드의 '위협 분석 리포트'에 실패 기록 추가.



## 4. 기술 스택 및 데이터 관리

* **Frontend/Backend:** Python Streamlit (단일 프레임워크)
* **LLM:**
* Google Gemini Pro (기본, `google-generativeai` 라이브러리 사용)
* Google Search Tool (Gemini API 내장 기능 활용)


* **데이터 저장 (No Backend 전략):**
* MVP 단계에서는 별도 DB 없이 Python `pandas` DataFrame과 `st.session_state`를 사용하여 메모리 상에서 관리.
* *공모전 시연 팁:* 앱이 재부팅되면 데이터가 날아가므로, 시연 중에는 앱을 끄지 않거나 로컬 `csv` 파일에 로그를 남기는 방식(Streamlit Cloud에서는 임시적임)을 혼용.



## 5. 프로젝트 파일 구조 (Directory Structure)

```text
security-vibe/
├── main.py                # 메인 앱 (대시보드 + 시나리오 생성 + 클릭 감지 로직 통합)
├── requirements.txt       # streamlit, google-generativeai, pandas 등
├── .streamlit/
│   └── secrets.toml       # (로컬용) API Key 및 SMTP 정보 저장
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py   # Gemini Search & Generate 로직
│   ├── email_sender.py    # SMTP 이메일 발송 함수
│   └── data_manager.py    # 훈련 이력/분석 데이터 관리 (CSV/Session State)
└── assets/
    └── warning_image.png  # 경고 페이지용 이미지

```