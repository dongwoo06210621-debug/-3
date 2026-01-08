import streamlit as st
import google.generativeai as genai

# ==========================================
# 👇 사용자님의 키 (수정 X)
FIXED_API_KEY = "AIzaSyCo9obJCHoqmJWdy1eIEWXfrrpRvXlGDxE"
# ==========================================

# 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")

st.title("🍽️ AI 메뉴 추천 도우미")
st.subheader("원하는 카테고리를 골라주세요!!")
st.write("---")


def recommend_menu(category):
    with st.spinner(f"AI가 맛있는 {category} 메뉴를 고르는 중... 🍳"):
        try:
            # 1. 키 설정
            genai.configure(api_key=FIXED_API_KEY)

            # 2. [핵심] 1.5 Flash 모델로 고정 (무료 사용량 넉넉함)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # 3. 질문 내용
            prompt = f"""
            너는 센스 있는 맛집 탐험가야. 사용자가 '{category}'를 먹고 싶어 해.
            1. 대중적이고 실패 없는 {category} 메뉴 하나를 추천해줘.
            2. 추천 이유를 짧고 재밌게 한 문장으로.
            """

            # 4. 답변 요청
            response = model.generate_content(prompt)

            # 5. 결과 출력
            st.success(f"추천 메뉴 ({category})")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")


# 버튼 배치 (4개씩 2줄)
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