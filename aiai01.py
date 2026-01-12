import streamlit as st
import google.generativeai as genai

# ==========================================
# ✅ [수정 완료] 이제 코드는 키를 직접 안 들고 있고, 금고(Secrets)에서 꺼내옵니다.
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception as e:
    st.error(f"🚨 Secrets 설정 오류: {e}")
    st.stop()
# ==========================================

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")
st.title("🍽️ AI 메뉴 추천 도우미 (2.5 버전)")
st.write("---")

def recommend_menu(category):
    with st.spinner(f"AI(2.5)가 {category} 메뉴를 생각 중... 🍳"):
        try:
            # 여기서 금고의 새 키를 가져옵니다.
            genai.configure(api_key=api_key)

            # 2.5 Flash 모델 사용
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"{category} 메뉴 하나 추천해주고 이유도 한 문장으로 말해줘."
            response = model.generate_content(prompt)
            st.success(f"추천: {response.text}")

        except Exception as e:
            st.error(f"오류: {e}")

# 버튼 배치
col1, col2 = st.columns(2)
with col1: st.button("🍚 한식", on_click=recommend_menu, args=("한식",))
with col2: st.button("🍜 중식", on_click=recommend_menu, args=("중식",))
with col3: st.button("🍝 양식", on_click=recommend_menu, args=("양식",))
with col4: st.button("🍣 일식", on_click=recommend_menu, args=("일식",))
with col5: st.button("🍲 아시안", on_click=recommend_menu, args=("아시안",))
with col6: st.button("🍜 분식", on_click=recommend_menu, args=("분식",))
with col7: st.button("🌮 퓨전", on_click=recommend_menu, args=("퓨전 요리",))
with col8: st.button("🍔 패스트푸드", on_click=recommend_menu, args=("패스트푸드",))