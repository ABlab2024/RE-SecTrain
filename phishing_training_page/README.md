# 피싱 훈련 경고 페이지 (Phishing Simulation Landing Page)

이 폴더는 피싱 훈련 이메일 내의 '더미 링크'를 클릭했을 때 사용자에게 보여줄 정적 웹페이지입니다.
사용자가 링크를 클릭하면 이 페이지가 나타나며, 이것이 훈련 상황임을 알리고 보안 수칙을 교육합니다.

## 📁 파일 구성
- `index.html`: 경고 및 교육 내용을 담은 메인 페이지
- `style.css`: 다크 모드, 글래스모피즘(Glassmorphism) 스타일이 적용된 CSS 디자인

## 🚀 사용 방법

### 옵션 1: 별도 호스팅 (추천)
이 폴더(`phishing_training_page`)의 내용물을 Netlify, Vercel, GitHub Pages 등을 통해 무료로 호스팅하세요.
호스팅 후 발급된 URL(예: `https://my-phishing-warning.netlify.app`)을 이메일 발송 코드의 링크 주소로 사용하면 됩니다.

**Netlify 배포 방법:**
1. [Netlify Drop](https://app.netlify.com/drop)에 접속합니다.
2. 이 `phishing_training_page` 폴더를 통째로 드래그 앤 드롭합니다.
3. 즉시 생성되는 URL을 복사하여 사용합니다.

### 옵션 2: Streamlit 앱 내에서 서빙
Streamlit 앱의 `static` 폴더 기능을 활용하여 이 파일을 서빙할 수도 있습니다.
1. 프로젝트 루트에 `static` 폴더를 만듭니다.
2. `index.html`과 `style.css`를 `static` 폴더로 옮깁니다.
3. 링크 주소를 `https://[여러분의-앱-주소]/app/static/index.html` 형태로 설정합니다. (Streamlit 버전에 따라 설정이 다를 수 있습니다)

## 📧 이메일 발송 코드 수정 예시 (utils/email_sender.py)

```python
# 기존 코드의 tracking_link 변수 부분을 호스팅된 주소로 변경하세요.
tracking_link = "https://your-deployed-warning-page.netlify.app" 
```

## 🎨 디자인 특징
- **시각적 임팩트**: 붉은색 계열의 경고 색상과 어두운 배경을 사용하여 사용자의 주의를 끕니다.
- **반응형 디자인**: PC와 모바일 모두에서 깨지지 않고 잘 보입니다.
- **교육적 콘텐츠**: 단순히 경고만 하는 것이 아니라, 어떤 위협이 있는지와 대처 방법을 구체적으로 안내합니다.
