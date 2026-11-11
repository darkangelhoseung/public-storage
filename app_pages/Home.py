import base64
import streamlit as st

st.title("AI 질문 답변 · 이미지 생성")

client = st.session_state["openai_client"]
api_key = st.session_state["api_key"]


@st.cache_data(show_spinner=False)
def get_answer(question, api_key):
    from openai import OpenAI

    response = OpenAI(api_key=api_key).responses.create(
        model="gpt-6-luna",
        input=question,
    )
    return response.output_text


st.header("질문 답변")

question = st.text_area("질문을 입력하세요.")

if st.button("답변 받기"):
    if question.strip():
        try:
            with st.spinner("답변 생성 중..."):
                st.session_state["home_answer"] = get_answer(
                    question, api_key
                )
        except Exception as e:
            st.error(f"오류: {e}")
    else:
        st.warning("질문을 입력하세요.")

if "home_answer" in st.session_state:
    st.write(st.session_state["home_answer"])

st.divider()
st.header("이미지 생성")

prompt = st.text_area("만들고 싶은 이미지를 설명하세요.")

if st.button("이미지 생성"):
    if prompt.strip():
        try:
            with st.spinner("이미지 생성 중..."):
                result = client.images.generate(
                    model="gpt-image-2.6-flare",
                    prompt=prompt,
                )
                st.session_state["generated_image"] = (
                    base64.b64decode(result.data[0].b64_json)
                )
        except Exception as e:
            st.error(f"오류: {e}")
    else:
        st.warning("이미지 설명을 입력하세요.")

if "generated_image" in st.session_state:
    st.image(st.session_state["generated_image"])
    