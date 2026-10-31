"""Chat screen for generating Jira test cases."""

import re
from pathlib import Path

import streamlit as st

from config_store import load_config
from act_parser import parse_act, render_table
from jira_client import fetch_ticket
from llm_client import generate


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "testcase_creator.md"
JIRA_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")


def build_prompt(ticket: dict) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    requirements = (
        f"Jira key: {ticket['key']}\n"
        f"Summary: {ticket['summary']}\n"
        f"Description: {ticket['description']}\n"
        f"Acceptance criteria: {ticket['acceptance_criteria']}"
    )
    return template.replace("[NUMBER]", "5").replace("[PASTE REQUIREMENTS HERE]", requirements)


st.set_page_config(page_title="Jira Test Case Generator", page_icon="✅", layout="centered")
st.title("Jira test case generator")
st.caption("Turn one Jira ticket into a structured test-case draft.")

with st.sidebar:
    st.header("ACT parser")
    act_file = st.file_uploader("Upload an .act test script", type=["act"])
    if act_file is not None:
        try:
            act_rows = parse_act(act_file.getvalue().decode("utf-8"))
            st.success(f"Parsed {len(act_rows)} test cases")
        except (UnicodeDecodeError, ValueError) as error:
            st.error(f"Could not parse ACT file: {error}")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if act_file is not None and "act_rows" in locals():
    st.subheader("Parsed test cases")
    st.markdown(render_table(act_rows), unsafe_allow_html=True)
    st.download_button(
        "Download markdown",
        render_table(act_rows),
        file_name=f"{act_file.name.rsplit('.', 1)[0]}.md",
        mime="text/markdown",
    )

with st.form("chat_form", clear_on_submit=True):
    request = st.text_input("Request", placeholder="Create test cases for QA-102")
    submitted = st.form_submit_button("Send", type="primary", use_container_width=True)

if submitted and request.strip():
    st.session_state.messages.append({"role": "user", "content": request.strip()})
    with st.chat_message("user"):
        st.markdown(request.strip())
    with st.chat_message("assistant"):
        key_match = JIRA_KEY_PATTERN.search(request.upper())
        if not key_match:
            answer = "Please include a Jira ticket key, for example `QA-102`."
        else:
            try:
                ticket = fetch_ticket(key_match.group(), load_config())
                answer, provider = generate(build_prompt(ticket), load_config())
                st.caption(f"Generated with {provider}")
            except Exception as error:
                answer = f"I could not generate test cases: {error}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
