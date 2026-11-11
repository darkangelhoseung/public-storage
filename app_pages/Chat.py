import streamlit as st

st.title("AI Chat")

client = st.session_state["openai_client"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def clear_chat():
    st.session_state["messages"] = []


st.button("Clear", on_click=clear_chat)

# 저장된 대화 표시
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def stream_text(events):
    for event in events:
        if event.type == "response.output_text.delta":
            yield event.delta


if prompt := st.chat_input("메시지를 입력하세요."):
    st.session_state["messages"].append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            stream = client.responses.create(
                model="gpt-6-luna",
                input=st.session_state["messages"],
                stream=True,
            )
            response = st.write_stream(stream_text(stream))

        st.session_state["messages"].append({
            "role": "assistant",
            "content": response,
        })

    except Exception as e:
        st.session_state["messages"].pop()
        st.error(f"오류가 발생했습니다: {e}")
        