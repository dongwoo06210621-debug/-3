import streamlit as st
import google.generativeai as genai

# ==========================================
# 🔒 비밀 금고(Secrets)에서 키 꺼내기
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 Secrets 설정 오류! Streamlit 사이트에 키를 넣어주세요.")
    st.stop()
# ==========================================

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")
st.title("🍽️ AI 메뉴 추천 도우미")
st.subheader("원하는 카테고리를 골라주세요!!")
st.write("---")


def get_best_model():
    """서버에서 사용 가능한 모델 명단을 가져와서 최신순으로 고릅니다."""
    try:
        # 1. 현재 키로 사용 가능한 모든 모델 조회
        model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

        # 2. 우선순위 설정 (2.5 -> 1.5 -> Pro 순서로 찾음)
        # 명단에 있는 것 중 가장 좋은 걸 return 함
        for model in model_list:
            if 'gemini-2.5' in model: return model
        for model in model_list:
            if 'gemini-1.5' in model: return model
        for model in model_list:
            if 'gemini-pro' in model: return model

        # 3. 만약 위 모델들이 없으면 목록의 첫 번째꺼라도 가져옴
        return model_list[0] if model_list else None

    except Exception:
        return None


def recommend_menu(category):
    # 모델 찾기
    genai.configure(api_key=api_key)
    target_model = get_best_model()

    if not target_model:
        st.error("❌ 사용 가능한 모델을 찾을 수 없습니다.")
        st.warning("원인: API 키가 잘못되었거나, 구글 서버에서 모델 목록을 불러오지 못했습니다.")
        return

    with st.spinner(f"AI({target_model} 연결됨)가 메뉴를 고르는 중... 🍳"):
        try:
            model = genai.GenerativeModel(target_model)

            prompt = f"""
            너는 센스 있는 맛집 탐험가야. 사용자가 '{category}'를 먹고 싶어 해.
            1. 대중적이고 실패 없는 {category} 메뉴 하나를 추천해줘.
            2. 추천 이유를 짧고 재밌게 한 문장으로.
            """

            response = model.generate_content(prompt)

            st.success(f"추천 메뉴 ({category})")
            st.caption(f"⚡ 연결된 모델: {target_model}")
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