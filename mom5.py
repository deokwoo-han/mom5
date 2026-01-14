import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import google.generativeai as genai

# --- 0. 기본 설정 및 디자인 ---
st.set_page_config(page_title="AI 솔빙 스트레스: LAMP 마스터", page_icon="🕯️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFBF5; }
    .main-header { font-size: 2.2rem; color: #E67E22; font-weight: bold; margin-bottom: 5px; }
    .sub-text { font-size: 1.1rem; color: #5D6D7E; margin-bottom: 20px; font-style: italic; }
    .card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #E67E22; }
    .sos-card { background-color: #F8F9F9; padding: 12px; border-radius: 10px; border: 1px solid #E0E0E0; margin-bottom: 10px; font-size: 14px; color: #555; }
    .sos-number { font-weight: bold; color: #E74C3C; font-size: 16px; }
    div.stButton > button:first-child { background-color: #E67E22; color: white; border-radius: 20px; border: none; padding: 10px 20px; font-weight: bold; }
    div.stButton > button:hover { background-color: #D35400; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 1. [책 내용 반영] LAMP 데이터 및 헬퍼 함수 ---

EMOTION_CHIPS = {
    "🔥 불안/공포": ["가슴이 뜀", "식은땀", "안절부절", "압박감", "질식감", "도망치고 싶음"],
    "💧 우울/슬픔": ["무기력", "눈물", "가라앉음", "허무함", "지침", "우울함"],
    "💢 분노/짜증": ["욱함", "답답함", "억울함", "신경질", "열받음", "미움"],
    "🌿 평온/긍정": ["다행임", "편안함", "감사함", "기대됨", "차분함", "후련함"]
}

# [책 내용 반영] 따뜻한 피드백 (책의 핵심 문구 인용)
def get_warm_feedback():
    quotes = [
        "걱정은 또 다른 걱정을 낳습니다. 지금 멈추셔도 좋습니다.",
        "미래는 통제할 수 없습니다. 당신이 통제할 수 있는 건 '지금 이 순간' 뿐입니다.",
        "불안은 당신을 해치지 않습니다. 그저 지나가는 파도일 뿐입니다.",
        "당신이 걱정하는 일의 90%는 실제로 일어나지 않습니다.",
        "생각과 사실을 구분하세요. 생각은 현실이 아닙니다."
    ]
    return random.choice(quotes)

if 'journal_logs' not in st.session_state: st.session_state.journal_logs = []
if 'ai_observer_text' not in st.session_state: st.session_state.ai_observer_text = ""
if 'ai_report_text' not in st.session_state: st.session_state.ai_report_text = ""
if 'comm_result' not in st.session_state: st.session_state.comm_result = ""

# --- 2. AI 기능 함수 (책의 이론 적용) ---

def get_ai_response(api_key, model_name, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 연결 오류: {str(e)}"

# --- 3. 사이드바 ---
with st.sidebar:
    st.title("🕯️ LAMP 마스터")
    st.caption("걱정이 많은 사람을 위한 심리학 수업")
    
    if st.session_state.journal_logs:
        st.caption(f"📝 누적 기록: **{len(st.session_state.journal_logs)}건**")
    
    st.divider()
    st.subheader("🔑 AI 설정")
    api_key = st.text_input("Google Gemini API Key", type="password")
    model_option = st.selectbox("모델 선택", ("Gemini 1.5 Flash (빠름)", "Gemini 1.5 Pro (정밀함)"))
    selected_model = "gemini-1.5-flash" if "Flash" in model_option else "gemini-1.5-pro"

    # [책 내용 반영] 메뉴 구조 개편
    menu = st.radio("LAMP 커리큘럼", 
        ["1단계: 걱정 이름표 붙이기", 
         "2단계: AI 심리 분석", 
         "3단계: 관계 테라피 (대화법)", 
         "4단계: 이완과 멈춤 (SOS)"])

# --- 4. 메인 화면 ---

st.markdown("<div class='main-header'>걱정 지우개: LAMP 프로젝트</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-text'>{get_warm_feedback()}</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [TAB 1] LAMP 1단계: 걱정 이름표 붙이기 (Labeling)
# -----------------------------------------------------------------------------
if menu == "1단계: 걱정 이름표 붙이기":
    st.info("💡 **LAMP 1단계:** 불안의 정체를 파악하고 이름표를 붙여 객관화하는 과정입니다.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='card'><h4>💭 1. 상황과 생각 포착</h4>", unsafe_allow_html=True)
        thought_input = st.text_area("걱정되는 상황 입력", height=100, placeholder="예: 내일 회의에서 말실수를 할까 봐 두렵다.")
        
        # [책 내용 반영] 걱정의 종류 세분화 (메타걱정 포함)
        st.markdown("<b>🏷️ 걱정의 종류 (이름표)</b>", unsafe_allow_html=True)
        label_type = st.radio("걱정의 종류", 
            ["실제적인 걱정 (해결 가능)", "가상의 걱정 (미래/통제 불가능)", "메타 걱정 (걱정에 대한 걱정)", "단순한 사실"], 
            horizontal=False)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'><h4>❤️ 2. 감정과 신체 반응</h4>", unsafe_allow_html=True)
        selected_emotions = []
        for cat, keys in EMOTION_CHIPS.items():
            selected_emotions.extend(st.multiselect(cat, keys))
        st.divider()
        intensity = st.slider("불안 농도", 0, 100, 50)
        sensation = st.text_input("신체 감각", placeholder="예: 어깨가 굳고 호흡이 얕다.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h4>🕵️ 3. 제3자의 시선 (거리두기)</h4>", unsafe_allow_html=True)
    
    if st.button(f"🤖 AI({selected_model})에게 객관적 시선 부탁하기"):
        if api_key and thought_input:
            with st.spinner("LAMP 이론에 따라 거리두기 중..."):
                # [책 내용 반영] 프롬프트에 LAMP 이론 주입
                prompt = f"""
                당신은 '걱정이 많은 사람을 위한 심리학 수업'의 저자이자 LAMP 치료 전문가입니다.
                사용자의 걱정: "{thought_input}"
                감정: {selected_emotions}
                라벨: {label_type}
                
                위 내용을 바탕으로 다음을 수행하세요:
                1. 이 걱정이 '통제 불가능한 미래'인지 '통제 가능한 현재'인지 구분해줄 것.
                2. 감정과 사실을 분리하여 건조한 3인칭 관찰자 시점으로 서술할 것.
                3. "당신이 걱정하는 일은 일어나지 않는다"는 뉘앙스의 안심 메시지로 끝맺을 것.
                """
                st.session_state.ai_observer_text = get_ai_response(api_key, selected_model, prompt)
    
    observer_view = st.text_area("관찰 기록", value=st.session_state.ai_observer_text, height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ 1단계 기록 저장하기", use_container_width=True):
        if thought_input:
            st.session_state.journal_logs.append({
                "time": datetime.now().strftime("%m-%d %H:%M"), "thought": thought_input,
                "emotions": selected_emotions, "intensity": intensity, "label": label_type, "observer": observer_view
            })
            st.session_state.ai_observer_text = ""
            st.success("기록되었습니다. 이제 걱정은 종이(화면) 위에 묶여있습니다."); time.sleep(1); st.rerun()

# -----------------------------------------------------------------------------
# [TAB 2] LAMP 2단계: 통제 욕구 버리기 (AI 분석)
# -----------------------------------------------------------------------------
elif menu == "2단계: AI 심리 분석":
    st.info("💡 **LAMP 2~3단계:** 통제할 수 없는 것을 받아들이고(Accepting), 현재에 집중(Mindfulness)합니다.")
    
    if not st.session_state.journal_logs:
        st.warning("분석할 데이터가 없습니다. 1단계에서 먼저 기록해주세요.")
    else:
        st.markdown("### 📈 불안 패턴 모니터링")
        df = pd.DataFrame(st.session_state.journal_logs)
        st.line_chart(df, x="time", y="intensity", color="#E67E22")
        
        st.divider()
        st.markdown("### 📑 LAMP 종합 심리 리포트")
        
        if st.button("🧠 종합 정밀 분석 실행"):
            if not api_key: st.error("API Key가 필요합니다.")
            else:
                with st.spinner("LAMP 모델로 분석 중..."):
                    logs_text = str(st.session_state.journal_logs)
                    # [책 내용 반영] 프롬프트 고도화
                    prompt = f"""
                    당신은 LAMP 심리치료 전문가입니다. 내담자의 기록({logs_text})을 분석하세요.
                    
                    [분석 포인트]
                    1. **메타 걱정 탐지**: 걱정에 대해 또 걱정하는 패턴이 보이는가?
                    2. **통제 욕구 분석**: 통제할 수 없는 미래를 통제하려다 생긴 불안인가?
                    3. **인지적 오류**: 재앙화, 흑백논리, 일반화의 오류가 있는가?
                    
                    [처방전]
                    - 내담자가 당장 놓아버려야 할 '통제 욕구'가 무엇인지 지적해줄 것.
                    - '현재 순간'에 집중할 수 있는 구체적인 행동 미션을 줄 것.
                    """
                    st.session_state.ai_report_text = get_ai_response(api_key, selected_model, prompt)
        
        if st.session_state.ai_report_text:
            st.markdown(f"<div class='card'>{st.session_state.ai_report_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [TAB 3] 관계 테라피 (책 2부 내용: 단호하게 말하기) - NEW!
# -----------------------------------------------------------------------------
elif menu == "3단계: 관계 테라피 (대화법)":
    st.info("💡 **관계 테라피:** 책에서 강조한 '나 전달법(I-Message)'을 연습합니다. 사실과 감정을 구분하여 요청하는 훈련입니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 😤 나의 상황 (Input)")
        fact = st.text_input("1. 사실 (Fact): 상대방이 구체적으로 어떤 행동을 했나요?", placeholder="예: 약속 시간에 30분 늦게 왔다.")
        emotion = st.text_input("2. 감정 (Emotion): 그래서 내 기분이 어땠나요?", placeholder="예: 무시받는 기분이고 속상했다.")
        request = st.text_input("3. 요청 (Request): 구체적으로 무엇을 원하나요?", placeholder="예: 늦을 것 같으면 미리 연락해줘.")
        
    with col2:
        st.markdown("#### 💬 AI 코칭 (Output)")
        st.write("공격적이지 않고 단호하게 말하는 법을 AI가 다듬어 드립니다.")
        
        if st.button("🗣️ 세련된 대화로 변환하기"):
            if api_key and fact:
                with st.spinner("비폭력 대화 모델 적용 중..."):
                    # [책 내용 반영] 대화법 프롬프트
                    prompt = f"""
                    사용자는 지금 누군가에게 불만을 표현하고 싶어합니다.
                    책 '걱정이 많은 사람을 위한 심리학 수업'에 나오는 [사실-감정-요청] 대화법에 따라 문장을 다듬어주세요.
                    
                    입력: 사실('{fact}'), 감정('{emotion}'), 요청('{request}')
                    
                    규칙:
                    1. '너' 주어(You-message)를 피하고 '나' 주어(I-message)를 사용할 것.
                    2. 비난하거나 공격적인 단어를 제거할 것.
                    3. 정중하지만 단호하게 의사를 전달하는 문장 2~3가지를 추천해줄 것.
                    """
                    st.session_state.comm_result = get_ai_response(api_key, selected_model, prompt)
            else:
                st.warning("내용과 API 키를 확인하세요.")
                
        if st.session_state.comm_result:
             st.success(st.session_state.comm_result)

# -----------------------------------------------------------------------------
# [TAB 4] 이완과 멈춤 (책 내용: 호흡 & 근육 이완)
# -----------------------------------------------------------------------------
elif menu == "4단계: 이완과 멈춤 (SOS)":
    st.markdown("<div class='card' style='border-left: 5px solid #E74C3C;'><h3>🚨 긴급 멈춤 버튼</h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌬️ 4-7-8 호흡법", "💪 점진적 근육 이완법"])
    
    with tab1:
        st.write("불안할 때 가장 먼저 해야 할 일은 '호흡'을 통제하여 뇌에 안전 신호를 보내는 것입니다.")
        if st.button("호흡 가이드 시작"):
            with st.empty():
                for _ in range(3):
                    st.markdown("## 🌿 들이마세요 (4초)"); time.sleep(4)
                    st.markdown("## 😶 멈추세요 (7초)"); time.sleep(7)
                    st.markdown("## 💨 내쉬세요 (8초)"); time.sleep(8)
                st.markdown("## 🧡 편안해지셨나요?")

    with tab2:
        # [책 내용 반영] 근육 이완법 추가
        st.write("몸의 긴장을 풀면 마음의 긴장도 풀립니다. 힘을 꽉 주었다가 툭 푸는 과정을 반복하세요.")
        if st.button("근육 이완 가이드 시작"):
            stages = [
                ("✊ 주먹 꽉 쥐기", "양 주먹을 꽉 쥐세요! 더 세게!", 5),
                ("🖐 주먹 툭 풀기", "힘을 툭 푸세요. 손끝의 저릿함을 느끼세요.", 8),
                ("😖 어깨 으쓱하기", "어깨를 귀까지 잔뜩 올리세요! 긴장시키세요!", 5),
                ("😌 어깨 툭 떨구기", "어깨를 툭 떨어뜨리세요. 무겁게 내려놓으세요.", 8)
            ]
            with st.empty():
                for title, desc, sec in stages:
                    st.markdown(f"## {title}\n### {desc}")
                    time.sleep(sec)
                st.success("몸이 한결 가벼워졌습니다.")
                
    st.divider()
    c1, c2 = st.columns(2)
    with c1: st.markdown("📞 <b>자살예방</b> <span class='sos-number'>109</span>", unsafe_allow_html=True)
    with c2: st.markdown("📞 <b>위기상담</b> <span class='sos-number'>1577-0199</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)