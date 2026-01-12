import streamlit as st
import google.generativeai as genai

# =========================================================
# 🔒 비밀 금고(Secrets)에서 키를 꺼내는 코드
try:
    # 아까 Secrets 화면에 적은 이름(GOOGLE_API_KEY)이랑 똑같아야 합니다.
    apikey = st.secrets["GOOGLE_API_KEY"]
except:
    # 혹시나 키를 못 찾으면 에러 메시지를 띄움
    st.error("Secrets 설정이 안 되어 있어요! Streamlit 사이트 설정을 확인해주세요.")
    st.stop()

# 가져온 키로 설정
genai.configure(api_key=apikey)
# =========================================================

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")
st.title("🍽️ AI 메뉴 추천 도우미 (1.5 Flash)")
st.subheader("하루 1,500번 무료! 맘껏 골라보세요.")
st.write("---")

def recommend_menu(category):
    with st.spinner(f"AI가 맛있는 {category} 메뉴를 고르는 중... 🍳"):
        try:
            # 모델 설정 (1.5 Flash)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            너는 센스 있는 맛집 탐험가야. 사용자가 '{category}'를 먹고 싶어 해.
            1. 대중적이고 실패 없는 {category} 메뉴 하나를 추천해줘.
            2. 추천 이유를 짧고 재밌게 한 문장으로.
            """

            response = model.generate_content(prompt)
            st.success(f"추천 메뉴 ({category})")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

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