죄송합니다. 제가 말씀을 제대로 이해하지 못해 불편을 드렸습니다.

원하시는 대로 **[1. 개발 히스토리(파일 구조 1~4)]**와 **[2. 설치 및 실행 방법]**을 **단 하나의 `README.md` 코드 블록 안에** 모두 통합했습니다.

이 코드를 복사해서 `README.md` 파일에 덮어씌우시면 됩니다.

```markdown
# 🕯️ LAMP Master: AI 걱정 지우개 (심리 치유 솔루션)

> **"걱정은 없애는 것이 아니라, 관리하는 것입니다."** > 베스트셀러 <걱정이 많은 사람을 위한 심리학 수업>의 **LAMP 치유법**을 완벽하게 구현한 AI 멘탈 헬스케어 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?style=flat&logo=google&logoColor=white)

---

## 📂 Project Architecture & History (개발 과정 및 파일 구조)

본 프로젝트는 MVP(최소 기능 제품)에서 시작하여 최종 AI 모델 연동까지 **4단계로 발전**했습니다. 포트폴리오 검토 시 각 단계별 코드를 통해 개발 과정을 확인하실 수 있습니다.

```text
📂 lamp-master
├── 📄 mom.py            # [v1.0] MVP Prototype
│   └── 기본적인 감정 칩(Emotion Chips) 선택 및 단순 기록 저장 기능 구현
│   └── 사용자 입력 데이터 구조 설계 (Thought, Emotion, Intensity)
│
├── 📄 mom2.py           # [v2.0] LAMP 이론 도입
│   └── '걱정 기록'과 '일지 확인' 메뉴 분리
│   └── 인지 라벨링(Cognitive Labeling) 기능 추가: '생산적 걱정' vs '소모적 걱정' 분류
│
├── 📄 mom3.py           # [v3.0] UX/UI 및 Warm-Tech 적용
│   └── 대시보드 시각화(Line Chart) 도입으로 감정 변화 추적
│   └── 랜덤 응원 메시지(Warm Feedback) 및 카드형 디자인 시스템 구축
│
├── 📄 mom_universe.py   # [v4.0] Final Release (최종 완성본)
│   └── Google Gemini AI 실제 연동 (Flash/Pro 모델 선택 기능)
│   └── 책 <걱정이 많은...>의 4단계 실천법 완벽 구현
│   └── 관계 테라피(비폭력 대화법) 및 점진적 근육 이완 훈련(SOS) 탑재
│
├── 📄 requirements.txt  # 필수 라이브러리 목록 (Streamlit, Gemini, Pandas)
└── 📄 README.md         # 프로젝트 설명 문서

```

---

## 💻 Installation & Usage (설치 및 실행 방법)

로컬 환경(내 컴퓨터)에서 최종 버전인 **`mom_universe.py`**를 구동하기 위한 절차입니다.

### 1. 환경 설정 (Prerequisites)

* Python 3.9 이상이 설치되어 있어야 합니다.

### 2. 저장소 가져오기 (Clone)

```bash
git clone [https://github.com/your-username/lamp-master.git](https://github.com/your-username/lamp-master.git)
cd lamp-master

```

### 3. 필수 라이브러리 설치 (Dependencies)

동봉된 `requirements.txt`를 통해 필요한 패키지를 일괄 설치합니다.

```bash
pip install -r requirements.txt

```

### 4. 애플리케이션 실행 (Run App)

터미널에 아래 명령어를 입력하여 앱을 실행합니다.

```bash
streamlit run mom_universe.py

```

### 5. API 키 설정 (Setup)

앱 실행 후 브라우저 화면의 **좌측 사이드바(Sidebar)**에서 설정을 완료해야 합니다.

1. **Google Gemini API Key** 입력 (발급: [Google AI Studio](https://aistudio.google.com/app/apikey))
2. 사용할 AI 모델 선택 (Flash: 속도 중심 / Pro: 성능 중심)

---

## 🚀 Key Features (주요 기능 - v4.0 기준)

이 앱은 단순한 일기장이 아닙니다. 책 한 권의 심리 치료 과정을 4단계로 경험할 수 있습니다.

### 1️⃣ 1단계: 걱정 이름표 붙이기 (Labeling)

* **걱정 분류:** 실제적 걱정, 가상의 걱정, 메타 걱정(걱정에 대한 걱정) 등으로 세분화하여 선택.
* **AI 객관화(Distancing):** Gemini AI가 사용자의 상황을 '건조한 제3자의 시선'으로 서술하여 감정과 사실을 분리해줍니다.

### 2️⃣ 2단계: AI 심리 분석 (Analysis)

* **통제 욕구 분석:** 사용자의 기록을 분석하여 '통제할 수 없는 미래'를 통제하려는 인지적 오류를 탐지합니다.
* **종합 리포트:** 임상심리 전문가 페르소나를 가진 AI가 심층 분석 보고서와 행동 처방을 제공합니다.

### 3️⃣ 3단계: 관계 테라피 (Relationship)

* **비폭력 대화법(NVC):** 대인관계 갈등 상황을 입력하면, **[사실-감정-요청]** 화법으로 변환해줍니다.
* **AI 코칭:** 공격적인 언어를 순화하고, 단호하지만 부드럽게 거절/요청하는 문장을 생성합니다.

### 4️⃣ 4단계: 이완과 멈춤 (SOS)

* **4-7-8 호흡 가이드:** 화면의 애니메이션에 맞춰 따라 할 수 있는 호흡 훈련 도구.
* **점진적 근육 이완법(PMR):** 신체 부위별 긴장과 이완을 반복하는 가이드 제공.

---

## ⚠️ Disclaimer (면책 조항)

* 본 서비스는 심리적 안정을 돕는 **자기 돌봄(Self-care) 도구**이며, 의학적 진단이나 치료를 대체할 수 없습니다.
* 심각한 우울증이나 불안 장애를 겪고 계신 경우, 반드시 **'SOS 위기 지원'** 탭의 전문가 연락처를 통해 도움을 받으시길 바랍니다.

---

**Developed with 🧡 by [당신의 이름]**

```

```
