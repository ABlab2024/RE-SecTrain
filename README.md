# 🛡️ Security Vibe (RE-SecTrain)

**Security Vibe**는 조직 및 개인의 보안 인식을 제고하기 위해 설계된 AI 기반 피싱 훈련 및 보안 교육 플랫폼입니다. 
최신 생성형 AI(LLM)를 활용하여 사용자 맞춤형 피싱 시나리오를 생성하고, 실제와 유사한 이메일 훈련을 제공하여 보안 위협에 대한 대응 능력을 강화합니다.

## ✨ 주요 기능

- **🤖 AI 기반 피싱 시나리오 생성**: Google, OpenAI, Anthropic 등의 LLM을 활용하여 쇼핑, 금융, 사내 공지 등 다양한 주제의 정교한 피싱 이메일을 자동으로 생성합니다.
- **📧 이메일 발송 및 추적**: 생성된 시나리오를 바탕으로 훈련 대상에게 이메일을 발송하고, 본문 내 링크 클릭 여부를 추적합니다.
- **🚨 실시간 교육 페이지**: 사용자가 훈련용 피싱 링크를 클릭할 경우, 즉시 경고 페이지(`phishing_training_page`)로 리다이렉트되어 피싱 식별 방법과 보안 수칙을 교육합니다.
- **📊 보안 대시보드**: 최신 보안 뉴스 트렌드를 요약하여 보여주고, 훈련 성과 및 취약점 리포트를 시각화하여 제공합니다.
- **📝 훈련 이력 관리**: 발송된 훈련 내역과 사용자의 반응(클릭 여부)을 기록하여 보안 수준을 모니터링합니다.

## 🛠️ 기술 스택

- **Language**: Python 3.x
- **Framework**: [Streamlit](https://streamlit.io/) (Web Interface)
- **AI/LLM**: LangChain / Custom LLM Client (Google Gemini, OpenAI GPT, Anthropic Claude 지원)
- **Data Management**: Pandas & Streamlit Session State (현재 버전은 세션 기반 데이터 저장)
- **Frontend (Warning Page)**: HTML5, CSS3 (Glassmorphism Design)

## 📂 프로젝트 구조

```bash
RE-SecTrain/
├── main.py                   # 메인 애플리케이션 진입점 (Streamlit)
├── utils/
│   ├── data_manager.py       # 데이터 관리 (훈련 이력, 리포트 등)
│   ├── email_sender.py       # 이메일 발송 모듈
│   └── llm_client.py         # LLM 연동 및 시나리오 생성 모듈
├── phishing_training_page/   # 피싱 경고 교육용 정적 페이지
│   ├── index.html
│   └── style.css
├── requirements.txt          # 의존성 패키지 목록
└── README.md                 # 프로젝트 설명 파일
```

## 🚀 설치 및 실행 방법

### 1. 환경 설정

먼저 프로젝트를 클론하고 가상환경을 설정하는 것을 권장합니다.

```bash
git clone https://github.com/your-repo/RE-SecTrain.git
cd RE-SecTrain

# 가상환경 생성 (선택 사항)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

필요한 Python 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

Streamlit을 사용하여 앱을 실행합니다.

```bash
streamlit run main.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱을 확인할 수 있습니다.

## ⚙️ 설정 가이드

1. **로그인**: 사이드바에서 이메일 주소를 입력하여 로그인합니다.
2. **AI 설정**: 사용할 LLM 공급자(Google, OpenAI 등)를 선택하고 API Key를 입력합니다.
3. **이메일 설정**: 실제 이메일 발송을 위해서는 `utils/email_sender.py` 또는 `secrets.toml` 파일에 SMTP 설정이 필요할 수 있습니다. (현재 개발 환경에 맞게 구성 필요)

## ⚠️ 주의사항

이 도구는 **교육 및 훈련 목적**으로만 사용해야 합니다. 사전 동의 없는 타인에게 피싱 이메일을 발송하는 행위는 불법이며 윤리적으로 금지되어 있습니다. 개발자는 이 도구의 오용으로 인한 책임질 지지 않습니다.

---
© 2026 Security Vibe Project. All rights reserved.
