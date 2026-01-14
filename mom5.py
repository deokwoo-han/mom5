import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import google.generativeai as genai

# --- 0. 기본 설정 및 디자인 ---
st.set_page_config(page_title="AI 솔빙 스트레스: 마음 닥터", page_icon="🧡", layout="wide")

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
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #FAE5D3; border-radius: 10px 10px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #E67E22; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 1. 데이터 및 헬퍼 함수 ---

EMOTION_CHIPS = {
    "🔥 불안/공포": ["가슴이 뜀", "식은땀", "안절부절", "압박감", "막막함", "초조함"],
    "💧 우울/슬픔": ["무기력", "눈물", "가라앉음", "허무함", "지침", "우울함"],
    "💢 분노/짜증": ["욱함", "답답함", "억울함", "신경질", "열받음", "미움"],
    "🌿 평온/긍정": ["다행임", "편안함", "감사함", "기대됨", "차분함", "후련함"]
}

# [복구됨] 따뜻한 피드백 메시지 함수
def get_warm_feedback():
    quotes = [
        "당신의 감정은 틀리지 않았습니다. 그저 날씨처럼 지나가는 중입니다. ☁️",
        "기록하는 것만으로도 당신은 이미 자신을 돌보고 계십니다. 👏",
        "불안은 당신이 잘하고 싶다는 마음의 증거이기도 합니다. 🌱",
        "잠시 심호흡을 해보세요. 지금 이 순간은 안전합니다. 🧘",
        "천천히 가도 괜찮습니다. 방향만 잃지 않는다면요. 🐢"
    ]
    return random.choice(quotes)

# 세션 상태 초기화
if 'journal_logs' not in st.session_state:
    st.session_state.journal_logs = []
if 'ai_observer_text' not in st.session_state:
    st.session_state.ai_observer_text = ""
if 'ai_report_text' not in st.session_state:
    st.session_state.ai_report_text = ""

# --- 2. AI 기능 함수 (Gemini) ---

# 개별 기록 객관화 (Flash/Pro 모델 선택 반영)
def get_ai_observer_view(api_key, model_name, thought, emotions, label):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        당신은 인지행동치료 전문가입니다. 아래 내용을 '제3자의 건조한 관찰자 시점'에서 3문장 이내로 서술해주세요.
        사용자 입력: 상황({thought}), 감정({', '.join(emotions)}), 라벨({label}).
        규칙: 주어는 '그/그녀'로 할 것. 사실과 감정을 분리할 것. 따뜻한 지지로 끝맺을 것. 한국어로 작성.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 연결 오류 ({model_name}): {str(e)}"

# 종합 심리 리포트
def get_comprehensive_report(api_key, model_name, logs):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        logs_text = ""
        for log in logs:
            logs_text += f"- [{log['time']}] 감정: {', '.join(log['emotions'])}, 농도: {log['intensity']}, 상황: {log['thought']}\n"
        
        prompt = f"""
        당신은 베테랑 임상심리 전문가입니다. 아래는 내담자의 최근 마음 기록 로그입니다.
        이를 분석하여 '종합 심리 분석 보고서'를 작성해주세요.
        
        [로그 데이터]
        {logs_text}
        
        [보고서 양식]
        1. **종합 소견**: 내담자의 주된 감정 패턴과 심리 상태 요약
        2. **발견된 인지 왜곡**: 기록에서 보이는 반복적인 부정적 사고 패턴 (예: 재앙화, 흑백논리 등)
        3. **전문가 처방**: 당장 실천할 수 있는 행동 가이드 2가지 (구체적으로)
        
        톤앤매너: 전문적이지만 따뜻하고 수용적인 어조. 한국어로 작성.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"분석 중 오류가 발생했습니다: {str(e)}"

# --- 3. 사이드바 (설정 & 현황) ---
with st.sidebar:
    st.title("🧡 마음 닥터")
    
    # [복구됨] 미니 대시보드
    if st.session_state.journal_logs:
        st.caption(f"📝 누적 기록: **{len(st.session_state.journal_logs)}건**")
        st.caption(f"🕒 최근 기록: {st.session_state.journal_logs[-1]['time']}")
    else:
        st.caption("아직 기록이 없습니다.")
    
    st.divider()
    
    st.subheader("🔑 AI 설정")
    api_key = st.text_input("Google Gemini API Key", type="password")
    
    st.caption("🤖 모델 선택")
    model_option = st.selectbox(
        "사용할 모델",
        ("Gemini 1.5 Flash (빠름)", "Gemini 1.5 Pro (정밀함)"),
        index=0
    )
    if "Flash" in model_option:
        selected_model = "gemini-1.5-flash"
    else:
        selected_model = "gemini-1.5-pro"

    if not api_key:
        st.info("AI 기능을 사용하려면 키를 입력하세요.")
        
    st.divider()
    menu = st.radio("메뉴 이동", ["📝 오늘의 마음 기록", "📊 AI 심리 분석", "🚨 SOS 위기 지원"])

# --- 4. 메인 화면 ---

st.markdown("<div class='main-header'>AI 솔빙 스트레스: 마음 관찰 일기</div>", unsafe_allow_html=True)
# [복구됨] 따뜻한 랜덤 문구 출력
st.markdown(f"<div class='sub-text'>{get_warm_feedback()}</div>", unsafe_allow_html=True)

# [TAB 1] 마음 기록
if menu == "📝 오늘의 마음 기록":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='card'><h4>💭 1. 상황과 생각</h4>", unsafe_allow_html=True)
        thought_input = st.text_area("생각/상황 입력", height=100, placeholder="예: 발표를 망칠까 봐 걱정된다.")
        label_type = st.radio("인지 라벨링", ["미래 불안 (What if)", "과거 후회 (If only)", "단순 사실", "해결 가능"], horizontal=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'><h4>❤️ 2. 감정과 감각</h4>", unsafe_allow_html=True)
        selected_emotions = []
        for cat, keys in EMOTION_CHIPS.items():
            selected_emotions.extend(st.multiselect(cat, keys))
        st.divider()
        intensity = st.slider("감정 농도 (0~100)", 0, 100, 50)
        sensation = st.text_input("신체 감각", placeholder="예: 심장이 쿵쿵거림")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><h4>🕵️ 3. 제3자의 시선 (AI 객관화)</h4>", unsafe_allow_html=True)
    
    if st.button(f"🤖 AI({selected_model})에게 객관적 시선 부탁하기"):
        if api_key and thought_input:
            with st.spinner(f"{model_option} 모델이 분석 중입니다..."):
                st.session_state.ai_observer_text = get_ai_observer_view(api_key, selected_model, thought_input, selected_emotions, label_type)
        else:
            st.warning("내용을 입력하고 API 키를 확인해주세요.")
    
    observer_view = st.text_area("관찰 기록 (수정 가능)", value=st.session_state.ai_observer_text, height=100)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("✨ 오늘의 마음 저장하기", use_container_width=True):
        if thought_input:
            st.session_state.journal_logs.append({
                "time": datetime.now().strftime("%m-%d %H:%M"),
                "thought": thought_input,
                "emotions": selected_emotions,
                "intensity": intensity,
                "label": label_type,
                "observer": observer_view
            })
            st.session_state.ai_observer_text = ""
            st.success("안전하게 기록되었습니다.")
            time.sleep(1)
            st.rerun()

    # 최근 기록 리스트
    st.divider()
    st.subheader("📂 최근 기록")
    if st.session_state.journal_logs:
        for log in reversed(st.session_state.journal_logs[-3:]):
            with st.expander(f"📌 {log['time']} | {log['thought'][:20]}..."):
                st.write(f"**감정:** {', '.join(log['emotions'])} ({log['intensity']}%)")
                st.markdown(f"**AI 관찰:** {log['observer']}")

# [TAB 2] AI 심리 분석
elif menu == "📊 AI 심리 분석":
    if not st.session_state.journal_logs:
        st.warning("데이터가 부족합니다. 먼저 기록을 남겨주세요.")
    else:
        st.markdown("### 📈 마음 건강 대시보드")
        df = pd.DataFrame(st.session_state.journal_logs)
        st.line_chart(df, x="time", y="intensity", color="#E67E22")
        
        st.divider()
        st.markdown("### 📑 AI 종합 심리 리포트")
        st.caption(f"선택된 모델: **{model_option}**")
        
        if st.button("🧠 종합 정밀 분석 실행"):
            if not api_key:
                st.error("API Key가 필요합니다.")
            else:
                with st.spinner("임상 데이터를 통합 분석 중입니다..."):
                    report = get_comprehensive_report(api_key, selected_model, st.session_state.journal_logs)
                    st.session_state.ai_report_text = report
        
        if st.session_state.ai_report_text:
            st.markdown(f"""
            <div class='card'>
                {st.session_state.ai_report_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

# [TAB 3] SOS 위기 지원
elif menu == "🚨 SOS 위기 지원":
    st.markdown("<div class='card' style='border-left: 5px solid #E74C3C;'>", unsafe_allow_html=True)
    st.error("### 혼자 감당하기 힘드신가요?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='sos-card'>📞 <b>자살예방</b> <span class='sos-number'>109</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='sos-card'>📞 <b>위기상담</b> <span class='sos-number'>1577-0199</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='sos-card'>🏥 <b>센터찾기</b><br>보건복지부 홈페이지</div>", unsafe_allow_html=True)
        st.markdown("<div class='sos-card'>💬 <b>청소년 상담</b><br>'다 들어줄 개' 앱</div>", unsafe_allow_html=True)
    
    st.divider()
    # [복구됨] 호흡 안정화 가이드
    st.subheader("🧘 긴급 안정화 (Grounding)")
    st.write("화면을 보며 천천히 호흡하세요.")
    if st.button("호흡 가이드 시작"):
        with st.empty():
            for _ in range(2): # 2세트 반복
                st.markdown("## 🌿 숨을 들이마시세요... (4초)")
                time.sleep(4)
                st.markdown("## 😶 숨을 멈추세요... (7초)")
                time.sleep(7)
                st.markdown("## 💨 숨을 내쉬세요... (8초)")
                time.sleep(8)
            st.success("조금 편안해지셨기를 바랍니다.")
    st.markdown("</div>", unsafe_allow_html=True)