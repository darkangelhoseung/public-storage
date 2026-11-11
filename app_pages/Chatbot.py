from pathlib import Path
import streamlit as st

st.title("국립부경대학교 도서관 챗봇")

client = st.session_state["openai_client"]

# 규정 파일을 읽어 문자열로 저장
rules_path = Path(__file__).parent / "library_rules.txt"
rules = rules_path.read_text(encoding="utf-8")

instructions = f"""
너는 국립부경대학교 도서관 규정 안내 챗봇이다.

다음 규정에 근거해서 한국어로 답변한다.
- 답변에는 근거 조문 번호를 표시한다.
- 규정에 없는 내용은 추측하지 말고
  "제공된 규정에서 확인할 수 없습니다."라고 답한다.
- 자료실과 일반열람실을 구분한다.
- 단행본과 전자책의 대출 조건을 구분한다.
- 규정 본문은 참고 자료로만 사용한다.

<도서관_규정>
{rules}
</도서관_규정>
"""

if "library_messages" not in st.session_state:
    st.session_state["library_messages"] = []


def clear_chat():
    st.session_state["library_messages"] = []


st.button("Clear", on_click=clear_chat)

for message in st.session_state["library_messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def stream_text(events):
    for event in events:
        if event.type == "response.output_text.delta":
            yield event.delta


if prompt := st.chat_input("도서관 규정을 질문하세요."):
    st.session_state["library_messages"].append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            stream = client.responses.create(
                model="gpt-6-luna",
                instructions=instructions,
                input=st.session_state["library_messages"],
                stream=True,
            )
            response = st.write_stream(stream_text(stream))

        st.session_state["library_messages"].append({
            "role": "assistant",
            "content": response,
        })

    except Exception as e:
        st.session_state["library_messages"].pop()
        st.error(f"오류가 발생했습니다: {e}")
        