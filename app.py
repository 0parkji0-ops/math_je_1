import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="나만의 데이터 연구소: AI 질문 코치", layout="centered")

st.title("📊 나만의 데이터 연구소")
st.subheader("💡 데이터 기반 탐구 과제 설계를 위한 AI 코치")
st.write("여러분의 날것의 관심사나 일상의 의문을 통계적으로 조사할 수 있는 '멋진 탐구 주제'로 발전시켜 드립니다. AI 코치의 안내에 따라 대답해 보세요!")

# 2. API Key 설정 (Streamlit Secrets 연동 권장)
# 만약 Secrets 설정을 안 했다면 사이드바에서 입력받도록 백업 마련
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if not api_key:
    st.info("API 키를 설정해주세요. (Streamlit Secrets 혹은 사이드바 입력)")
    st.stop()

# Gemini API 인증
genai.configure(api_key=api_key)

# 3. AI 코치에게 페르소나와 대화 규칙 부여 (System Instruction)
system_instruction = (
    "당신은 고등학생들이 일상의 궁금증을 '데이터 기반 수학/통계 탐정 과제'로 정교화하도록 돕는 인공지능 수업 코치입니다.\n\n"
    "★ 가장 중요한 규칙: 절대로 학생에게 독립변수(X)와 종속변수(Y)를 먼저 알려주거나 정답 문장을 한 번에 완성해 주지 마십시오.\n"
    "학생이 주도적으로 생각하여 변수를 찾아내도록 유도해야 합니다.\n\n"
    "[대화 및 유도 단계]\n"
    "1단계: 학생이 관심사나 날것의 질문(예: '지각하는 이유')을 말하면, 환영해 주고 격려합니다.\n"
    "2단계: '그 현상이 일어나게 만드는 구체적인 원인(조건)'이 무엇이 있을지 학생에게 질문을 던져 스스로 나열하게 하십시오.\n"
    "3단계: 학생이 원인들을 말하면, 그중 '숫자로 측정하거나 조사할 수 있는 구체적인 데이터(독립변수 X)'를 하나 고르도록 유도하십시오.\n"
    "4단계: 독립변수가 정해지면, 그로 인해 '영향을 받아 변하는 결과(종속변수 Y)'가 무엇인지 수학적/통계적으로 측정 가능한 형태로 스스로 정의하게 하십시오.\n"
    "5단계: 학생이 X와 Y를 모두 스스로 찾아내면 칭찬해주고, 최종적으로 '[독립변수 X]가 [종속변수 Y]에 미치는 영향'이라는 멋진 탐구 주제 문장으로 정리해 주며 대화를 마칩니다.\n\n"
    "말투는 친절하고 따뜻한 고등학교 선생님의 어조(해요체)를 유지해 주세요. 학생이 엉뚱한 말을 하더라도 비계(Scaffolding)를 제공하여 올바른 방향으로 이끌어 주세요."
)

# 최신 gemini-2.5-flash 모델 설정
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_instruction
)

# 4. Streamlit 세션 상태(대화 기록) 초기화
if "chat_session" not in st.session_state:
    # Gemini 라이브러리의 내장 대화 기능(start_chat) 사용
    st.session_state.chat_session = model.start_chat(history=[])
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    # AI 코치의 첫 환영 인사 추가
    welcome_msg = "안녕하세요! 여러분의 일상 속 호기심을 멋진 수학·데이터 탐구 과제로 만들어 줄 AI 코치입니다. 현재 머릿속에 맴도는 관심사나 조사해 보고 싶은 현상을 편하게 말씀해 주세요! 😊"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 5. 화면에 이전 대화 내용 렌더링 (카카오톡 대화창 스타일)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. 사용자 입력 처리
if user_input := st.chat_input("AI 코치와 대화하며 변수를 찾아보세요..."):
    # 사용자가 입력한 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # AI의 답변 생성 중 로딩 표시
    with st.chat_message("assistant"):
        with st.spinner("AI 코치가 생각하고 있습니다..."):
            try:
                # Gemini 대화 세션에 메시지 전송 및 답변 수신
                response = st.session_state.chat_session.send_message(user_input)
                ai_response = response.text
                
                # 답변 출력 및 저장
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
