# public-storage
import streamlit as st
from openai import OpenAI

st.title("AI 질문 답변")

api_key = st.session_state["api_key"]


@st.cache_data(show_spinner=False)
def get_answer(question, api_key):
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-6-luna",
        input=question,
    )
    return response.output_text


question = st.text_area("질문을 입력하세요.")

if st.button("답변 받기"):
    if question.strip():
        try:
            with st.spinner("답변 생성 중..."):
                answer = get_answer(question, api_key)
            st.write(answer)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("질문을 입력하세요.")
import base64

st.divider()
st.header("AI 이미지 생성")

image_prompt = st.text_area(
    "만들고 싶은 이미지를 설명하세요.",
    key="image_prompt",
)

if st.button("이미지 생성"):
    if image_prompt.strip():
        try:
            client = st.session_state["openai_client"]

            with st.spinner("이미지 생성 중... 잠시 기다려 주세요."):
                img = client.images.generate(
                    model="gpt-image-2.6-flare",
                    prompt=image_prompt,
                )

                image_bytes = base64.b64decode(
                    img.data[0].b64_json
                )

            st.session_state["generated_image"] = image_bytes

        except Exception as e:
            st.error(f"이미지 생성 오류: {e}")
    else:
        st.warning("이미지 설명을 입력하세요.")

if "generated_image" in st.session_state:
    st.image(st.session_state["generated_image"])
    
