import streamlit as st
import google.generativeai as genai

# ==========================================
# 👇 여기에 키를 입력해 두었습니다! (따옴표 지우지 마세요)
FIXED_API_KEY = "AIzaSyDq4aWjGj4Sh4VX8aQwAGcWwrqe8lwXSiw"
# ==========================================

# 페이지 기본 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")

# 1. 메인 화면 설정
st.title("🍽️ AI 메뉴 추천 도우미")
st.subheader("먹고 싶은 카테고리를 골라보세요!")
st.write("---")


# 2. 메뉴 추천 함수
def recommend_menu(category):
    with st.spinner(f"AI가 맛있는 {category} 메뉴를 고르는 중... 🍳"):
        try:
            # 1. 고정된 키로 설정 (사이드바 입력 X)
            genai.configure(api_key=FIXED_API_KEY)

            # 2. 사용 가능한 모델 자동 찾기
            target_model = None
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    target_model = m.name
                    if 'flash' in m.name:  # 속도 빠른 모델 선호
                        break

            # 모델을 못 찾았을 경우 대비
            if not target_model:
                # 만약 리스트에서 못 찾으면 가장 기본 이름으로 강제 시도
                target_model = 'models/gemini-pro'

            model = genai.GenerativeModel(target_model)

            # 3. 질문 내용
            prompt = f"""
            너는 센스 있는 맛집 탐험가야. 사용자가 '{category}'를 먹고 싶어 해.
            1. 대중적이고 실패 없는 {category} 메뉴 하나를 추천해줘.
            2. 추천 이유를 짧고 재밌게 한 문장으로.
            """

            # 4. AI에게 질문
            response = model.generate_content(prompt)

            # 5. 결과 보여주기
            st.success(f"추천 메뉴 ({category})")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")


# 3. 버튼 배치 (누르면 바로 실행됨)
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