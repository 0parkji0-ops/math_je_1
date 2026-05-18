import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="특성화고 질문 심폐소생소", page_icon="🚀", layout="centered")

st.title("🚀 특성화고 맞춤형 질문 심폐소생소")
st.subheader("여러분의 호기심을 멋진 '데이터 탐구 주제'로 바꾸어 드립니다!")
st.write("---")

# API 키 설정 (스트림릿 비밀번호 설정이나 직접 입력 가능)
# 실제 수업 시에는 교사의 API 키를 환경변수에 숨겨두거나 입력창을 만듭니다.
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    st.warning("왼쪽 사이드바에 API Key를 입력해야 AI 코치가 작동합니다.")

# 2. 학생 입력 양식
with st.form("my_form"):
    st.write("### ✍️ 나만의 원래 질문 적기")
    original_q = st.text_input(
        "평소에 궁금했던 점이나 엉뚱한 질문도 괜찮아요!",
        placeholder="예시: 호텔 성수기 가격은 왜 비쌀까?, 수면시간이랑 집중력이 연관 있을까?"
    )
    
    st.write("### 🏨 내 질문과 가장 가까운 분야 선택")
    category = st.selectbox(
        "어떤 분야로 탐구해보고 싶나요?",
        ["호텔/관광/전공 실무 경영", "학교생활/청소년 심리/통계", "과학/실험/확률적 분석", "기타 일상 호기심"]
    )
    
    submitted = st.form_submit_button("AI 코치에게 피드백 받기 ⚡")

# 3. AI 코칭 프롬프트 엔진 작동
if submitted and api_key:
    if not original_q:
        st.error("질문을 입력해 주세요!")
    else:
        with st.spinner("AI 코치가 질문을 정교하게 다듬는 중..."):
            
            # AI의 역할을 규정하는 핵심 시스템 프롬프트
            system_prompt = f"""
            당신은 특성화고등학교 학생들을 대상으로 하는 친절하고 격려 넘치는 '데이터 탐구 주도성 코치'입니다.
            학생이 입력한 일상적이고 투박한 질문을 받아, 이를 수학적, 통계적, 과학적으로 증명 및 데이터 수집이 가능한 '진짜 탐구 질문'으로 리모델링해 주어야 합니다.

            [학생 정보]
            - 원래 질문: {original_q}
            - 선택한 분야: {category}

            [답변 양식 지침 - 반드시 다음 구조로 따뜻하게 응답할 것]
            1. 🎉 **공감과 칭찬**: 학생의 질문이 가진 참신함이나 실무적 가치를 친절한 말투(~요체)로 폭풍 칭찬해 주세요.
            2. 🛠️ **변수 매핑 (X와 Y 찾기)**: 이 질문을 데이터화하기 위해 조사해야 할 '원인[독립변수 X]'와 '결과[종속변수 Y]'를 명확히 짚어주세요.
            3. 📈 **업그레이드 탐구 주제 제안**: 고등학생 수준에서 구글 폼 설문조사, 크롤링, 데이터 수집을 통해 해결할 수 있는 멋진 탐구 주제 2가지를 제안해 주세요. (문장 속에 X와 Y가 명확히 드러나고 통계/함수/확률 개념과 연결되도록)
            4. 🏃 **다음 발자국**: 데이터를 모으기 위해 당장 내일 학교에서 무엇을 하면 좋을지(예: 설문조사 만들기, 웹사이트 가격 조사하기 등) 구체적인 미션을 던져주세요.
            """
            
            try:
                response = model.generate_content(system_prompt)
                st.write("---")
                st.success("✨ AI 코치의 심폐소생 완료!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")

st.write("---")
st.caption("© 2026 우리 학교 AI 융합 수업 프로젝트 - 질문이 데이터가 되는 순간")
