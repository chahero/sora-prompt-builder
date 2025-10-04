# Sora2 Script Builder 🎬

## 프로젝트 소개 (About This Project)

**Sora2 Script Builder**는 OpenAI의 Sora와 같은 AI 동영상 생성 모델을 위한 정교한 JSON 형식의 스크립트(프롬프트)를 손쉽게 만들 수 있도록 도와주는 웹 애플리케이션입니다. 사용자는 더 이상 복잡한 JSON 구조를 직접 작성할 필요 없이, 직관적인 UI를 통해 아이디어를 체계적인 비디오 스크립트로 완성할 수 있습니다.

이 앱은 사용자가 직접 ChatGPT나 Gemini 같은 LLM(거대 언어 모델)을 활용하여 스크립트 초안을 생성하고, 그 결과를 앱으로 가져와 세부적으로 편집 및 관리하는 워크플로우를 지원합니다.

---

## 🚀 Live Demo

이 앱은 Streamlit Community Cloud를 통해 배포되어 누구나 무료로 사용해 볼 수 있습니다.

**바로가기: https://sora-prompt-builder.streamlit.app/**

---

## 주요 기능 (Features)

- **🤖 LLM 프롬프트 생성기 (Prompt Generator for LLMs):**
    - 영상 주제, 길이, 스타일 등 몇 가지 조건만 입력하면, ChatGPT나 Gemini가 가장 잘 이해할 수 있는 **최적화된 지시문(프롬프트)을 생성**합니다.
- **📋 스크립트 불러오기 & 파싱 (Script Importer & Parser):**
    - LLM으로부터 생성된 JSON 형식의 스크립트를 붙여넣으면, 앱이 **자동으로 내용을 분석하고 편집 가능한 UI로 변환**합니다.
    - 키 이름이나 데이터 형식이 약간 다르더라도 지능적으로 처리하는 **강력한 파싱 기능**이 내장되어 있습니다.
- **🧠 템플릿 지원 (Templates):**
    - '제품 광고', '영화 예고편' 등 자주 사용되는 스크립트 구조를 **템플릿으로 제공**하여, 클릭 한 번으로 빠르게 작업을 시작할 수 있습니다.
- **✍️ 직관적인 스크립트 편집기 (Intuitive Script Editor):**
    - 영상 기본 정보와 각 장면의 상세 내용을 체계적으로 관리할 수 있습니다.
    - 장면을 **동적으로 추가, 수정, 삭제**하는 것이 가능합니다.
    - 깔끔한 탭(Tabs)과 컬럼(Columns) 레이아웃으로 복잡한 스크립트도 한눈에 파악할 수 있습니다.
- **📥 JSON 내보내기 (Export to JSON):**
    - 완성된 스크립트는 Sora 2에서 바로 사용할 수 있는 `.json` 파일로 언제든지 다운로드할 수 있습니다.

---

## 설치 및 실행 방법 (Installation & Usage)

이 프로젝트는 Python과 Streamlit 라이브러리를 기반으로 합니다.

### 사전 요구 사항 (Prerequisites)

- Python 3.8 이상

### 설치 (Installation)

1. **프로젝트 클론:**Bash
    
    `git clone https://github.com/your-username/sora-prompt-builder.git
    cd sora-prompt-builder`
    
2. **가상 환경 생성 및 활성화:**Bash
    
    `# Windows
    python -m venv .venv
    .venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate`
    
3. **필요한 라이브러리 설치:**Bash
    
    `pip install streamlit`
    

### 실행 (Running the App)

1. 프로젝트 폴더 내에서 아래 명령어를 터미널에 입력하세요.Bash
    
    `streamlit run app.py`
    
2. 명령어를 실행하면 자동으로 웹 브라우저에 새 탭이 열리면서 애플리케이션이 실행됩니다.

---

## 사용 흐름 (Workflow)

1. **[Tab 1] 프롬프트 생성:** 앱의 'LLM 프롬프트 생성' 탭에서 영상 아이디어를 입력하고, 생성된 지시문을 복사합니다.
2. **[ChatGPT / Gemini] 스크립트 초안 생성:** 복사한 지시문을 원하는 AI 챗봇에게 질문하여 JSON 형식의 스크립트 초안을 받습니다.
3. **[Tab 2] 스크립트 불러오기 및 편집:** AI가 생성한 JSON 결과를 '스크립트 편집' 탭에 붙여넣고 '불러오기' 버튼을 누릅니다.
4. **[Tab 2] 내용 수정:** UI 편집기를 통해 스크립트의 세부 내용을 원하는 대로 자유롭게 수정합니다.
5. **[Tab 3] 최종 결과 확인 및 다운로드:** 완성된 스크립트를 확인하고 `.json` 파일로 다운로드하여 사용합니다.

---

## 기여 방법 (Contributing)

이 프로젝트에 기여하고 싶으신 분들은 언제든지 환영입니다. 버그 리포트, 기능 제안 등은 GitHub 이슈(Issues)를 통해 남겨주시거나, 직접 수정하여 Pull Request를 보내주세요.