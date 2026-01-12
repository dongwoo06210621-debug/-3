import streamlit as st
import google.generativeai as genai

# ==========================================
# 🔒 비밀 금고(Secrets)에서 키 꺼내기
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 Secrets 설정이 없습니다! Streamlit 설정에 키를 넣어주세요.")
    st.stop()
# ==========================================

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")
st.title("🍽️ AI 메뉴 추천 도우미")
st.subheader("원하는 카테고리를 골라주세요!!")
st.write("---")

def recommend_menu(category):
    with st.spinner(f"AI(2.5)가 {category} 메뉴를 생각 중... 🍳"):
        try:
            genai.configure(api_key=api_key)

            # 🚨 [수정 완료] 님이 원하시는 대로 '2.5 Flash'로 고정했습니다.
            target_model = 'gemini-2.5-flash'

            model = genai.GenerativeModel(target_model)

            prompt = f"""
            너는 센스 있는 맛집 탐험가야. 사용자가 '{category}'를 먹고 싶어 해.
            1. 대중적이고 실패 없는 {category} 메뉴 하나를 추천해줘.
            2. 추천 이유를 짧고 재밌게 한 문장으로.
            """

            response = model.generate_content(prompt)

            st.success(f"추천 메뉴 ({category})")
            st.caption(f"⚡ 작동 모델: {target_model}")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            # 2.5 모델은 하루 20번 제한이 있어서, 그게 다 차면 에러가 날 수 있습니다.
            st.error(f"오류가 발생했습니다: {e}")
            if "429" in str(e):
                st.warning("⚠️ 2.5 모델의 하루 사용량(20회)을 초과한 것 같습니다.")

# 버튼 배치
col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

with col1: st.button("🍚 한식", on_click=recommend_menu, args=("한식",))
with col2: st.button("🍜 중식", on_click=recommend_menu, args=("중식",))
with col3: st.button("🍝 양식", on_click=recommend_menu, args=("양식",))
with col4: st.button("🍣 일식", on_click=recommend_menu, args=("일식",))
with col5: st.button("🍲 아시안", on_click=recommend_menu, args=("아시안",))
with col6: st.button("🍜 분식", on_click=recommend_menu, args=("분식",))
with col7: st.button("🌮 퓨전", on_click=recommend_menu, args=("퓨전 요리",))
with col8: st.button("🍔 패스트푸드", on_click=recommend_menu, args=("패스트푸드",))