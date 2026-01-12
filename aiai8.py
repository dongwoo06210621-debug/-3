import streamlit as st
import google.generativeai as genai

# ==========================================
# 🔒 [보안] 비밀 금고(Secrets)에서 키를 꺼내옵니다.
# (코드는 안전하고, 키는 사이트 설정에 숨겨져 있습니다)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 Secrets 설정이 없습니다! Streamlit 사이트의 [Settings] > [Secrets]에 키를 저장해주세요.")
    st.stop()
# ==========================================

# 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")

st.title("🍽️ AI 메뉴 추천 도우미")
st.subheader("원하는 카테고리를 골라주세요!!")
st.write("---")


def recommend_menu(category):
    with st.spinner(f"AI가 맛있는 {category} 메뉴를 고르는 중... 🍳"):
        try:
            # 1. 시크릿 키로 설정
            genai.configure(api_key=api_key)

            # -----------------------------------------------------------
            # 🤖 [유동적 선택] 상황에 맞춰 최적의 모델을 자동으로 찾습니다.
            target_model = 'gemini-1.5-flash'  # 1순위: 가성비 좋은 Flash

            try:
                # 현재 사용 가능한 모델 명단을 훑어봅니다.
                model_list = [m.name for m in genai.list_models()]

                # 명단에 'flash'가 아예 없으면 -> 구형 모델(Pro)로 자동 전환
                # (이렇게 하면 404 오류가 나도 죽지 않고 살아납니다)
                if not any('flash' in m for m in model_list):
                    target_model = 'gemini-pro'
            except:
                # 명단 조회조차 실패하면 그냥 기본값(Flash)으로 밀고 나갑니다.
                pass
            # -----------------------------------------------------------

            # 결정된 모델로 연결
            model = genai.GenerativeModel(target_model)

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
            # 어떤 모델이 선택되었는지 살짝 보여줍니다 (성공 확인용)
            st.caption(f"⚡ 연결된 모델: {target_model}")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.caption("💡 팁: 오류가 계속되면 Streamlit 사이트에서 앱을 'Reboot' 해보세요.")


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