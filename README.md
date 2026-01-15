네, **`mom_universe.py`** (LAMP 마스터 확장판)를 깃허브(GitHub)나 포트폴리오에 올리실 때 사용할 수 있는 **전문적인 `README.md**` 문서를 작성해 드립니다.

이 문서는 앱의 **기획 의도(심리학 이론), 주요 기능, 설치 방법, 사용법**을 체계적으로 정리하여 개발자와 사용자 모두가 쉽게 이해할 수 있도록 구성했습니다.

---

### 📄 `README.md` (복사해서 사용하세요)

아래 내용을 복사하여 **`README.md`** 파일을 만들고 붙여넣으시면 됩니다.

```markdown
# 🕯️ LAMP Master: AI 걱정 지우개 (심리 치유 솔루션)

> **"걱정은 없애는 것이 아니라, 관리하는 것입니다."** > 베스트셀러 <걱정이 많은 사람을 위한 심리학 수업>의 **LAMP 치유법**을 완벽하게 구현한 AI 멘탈 헬스케어 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?style=flat&logo=google&logoColor=white)

## 📖 프로젝트 소개 (Overview)

**LAMP Master**는 인지행동치료(CBT) 기반의 'LAMP 이론'을 디지털 환경으로 옮겨온 **Warm-Tech(따뜻한 기술)** 프로젝트입니다. 
사용자가 막연한 불안감에 압도되지 않도록 걱정에 이름표를 붙이고(Labeling), AI와의 상담을 통해 객관화하며, 호흡과 이완 훈련을 통해 현재에 집중하도록 돕습니다.

### 💡 LAMP 이론이란?
- **L (Labeling):** 불안의 실체에 이름표 붙이기 (인지적 명명)
- **A (Accepting):** 통제할 수 없는 것을 인정하고 수용하기
- **M (Mindfulness):** 현재의 감각과 호흡에 집중하기
- **P (Present):** 지금 이 순간 할 수 있는 행동 실천하기

---

## 🚀 주요 기능 (Key Features)

이 앱은 단순한 일기장이 아닙니다. 책 한 권의 심리 치료 과정을 4단계로 경험할 수 있습니다.

### 1️⃣ 1단계: 걱정 이름표 붙이기 (Labeling)
- **걱정 분류:** 실제적 걱정, 가상의 걱정, 메타 걱정(걱정에 대한 걱정) 등으로 세분화하여 선택.
- **감정 칩(Emotion Chips):** 텍스트로 표현하기 힘든 감정을 직관적인 칩으로 선택.
- **AI 객관화(Distancing):** Gemini AI가 사용자의 상황을 '건조한 제3자의 시선'으로 서술하여 감정과 사실을 분리해줍니다.

### 2️⃣ 2단계: AI 심리 분석 (Analysis)
- **통제 욕구 분석:** 사용자의 기록을 분석하여 '통제할 수 없는 미래'를 통제하려는 인지적 오류를 탐지합니다.
- **종합 리포트:** 임상심리 전문가 페르소나를 가진 AI가 심층 분석 보고서와 행동 처방을 제공합니다.
- **감정 그래프:** 날짜별 불안 농도의 변화를 시각화하여 보여줍니다.

### 3️⃣ 3단계: 관계 테라피 (Relationship)
- **비폭력 대화법(NVC):** 대인관계 갈등 상황을 입력하면, **[사실-감정-요청]** 화법으로 변환해줍니다.
- **AI 코칭:** 공격적인 언어를 순화하고, 단호하지만 부드럽게 거절/요청하는 문장을 생성합니다.

### 4️⃣ 4단계: 이완과 멈춤 (SOS)
- **4-7-8 호흡 가이드:** 화면의 애니메이션에 맞춰 따라 할 수 있는 호흡 훈련 도구.
- **점진적 근육 이완법(PMR):** 신체 부위별 긴장과 이완을 반복하는 가이드 제공.
- **위기 지원 정보:** 자살 예방 및 위기 상담 센터 핫라인 연결.

---

## 🛠️ 기술 스택 (Tech Stack)

- **Frontend/Backend:** Python, Streamlit (단일 코드베이스로 빠른 배포)
- **AI Engine:** Google Generative AI (Gemini 1.5 Flash & Pro 모델 선택 가능)
- **Data Analysis:** Pandas (시계열 데이터 처리 및 시각화)
- **Deployment:** Streamlit Cloud

---

## 💻 설치 및 실행 방법 (Installation)

로컬 환경에서 실행하려면 아래 절차를 따르세요.

**1. 저장소 클론 (Clone)**
```bash
git clone [https://github.com/your-username/lamp-master.git](https://github.com/your-username/lamp-master.git)
cd lamp-master

```

**2. 필수 패키지 설치**

```bash
pip install -r requirements.txt

```

**3. API 키 설정**

* 앱 실행 후 사이드바 설정창에 **Google Gemini API Key**를 입력해야 합니다.
* (키 발급: [Google AI Studio](https://aistudio.google.com/app/apikey))

**4. 앱 실행**

```bash
streamlit run mom_universe.py

```

---

## 📂 파일 구조 (File Structure)

```
📂 lamp-master
├── mom_universe.py      # 메인 애플리케이션 코드 (통합 버전)
├── requirements.txt     # 의존성 패키지 목록
└── README.md            # 프로젝트 설명 문서

```

---

## ⚠️ 면책 조항 (Disclaimer)

* 본 서비스는 심리적 안정을 돕는 **자기 돌봄(Self-care) 도구**이며, 의학적 진단이나 치료를 대체할 수 없습니다.
* 심각한 우울증이나 불안 장애를 겪고 계신 경우, 반드시 **'SOS 위기 지원'** 탭의 전문가 연락처를 통해 도움을 받으시길 바랍니다.

---

**Developed with 🧡 by [당신의 이름/팀명]**

```

### 📝 적용 가이드

1.  프로젝트 폴더 안에 `README.md`라는 새 파일을 만드세요.
2.  위의 코드 블록 내용을 **그대로 복사**해서 붙여넣으세요.
3.  맨 마지막 줄의 **[당신의 이름/팀명]** 부분만 본인 이름으로 수정하시면 됩니다.

이 `README.md`는 앱의 전문성을 보여주고, 심사위원이나 다른 개발자가 프로젝트를 이해하는 데 큰 도움이 될 것입니다!

```
