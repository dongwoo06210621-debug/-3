import streamlit as st
import google.generativeai as genai

# ==========================================
# 🔒 비밀 금고(Secrets)에서 키를 꺼내는 코드
# (이제 코드에 키가 노출되지 않아 안전합니다!)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 Secrets 설정이 안 되어 있습니다. Streamlit 사이트 설정(Settings)을 확인해주세요.")
    st.stop()
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
            # 1. 시크릿에서 가져온 키로 설정
            genai.configure(api_key=api_key)

            # 2. 사용 가능한 모델 자동 찾기 (가장 안정적인 방식)
            target_model = 'gemini-1.5-flash'  # 1순위: 최신 Flash 모델

            # (혹시 몰라 사용 가능한지 확인하는 절차)
            try:
                # 모델 목록을 가져와서 체크해봄 (버전 호환성 확인)
                available_models = [m.name for m in genai.list_models()]
                # 만약 목록에 Flash가 없으면 Pro로 변경 (404 오류 방지)
                if not any('flash' in m for m in available_models):
                    target_model = 'gemini-pro'
            except:
                pass  # 확인하다 에러나면 그냥 기본 설정(Flash)으로 시도

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
            st.caption(f"⚡ 작동 모델: {target_model}")
            st.markdown(f"### 🥘 {response.text}")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.write("💡 팁: 'requirements.txt' 파일에 'google-generativeai>=0.7.0'이 적혀 있는지 확인해주세요.")


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