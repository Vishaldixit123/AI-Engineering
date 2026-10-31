"""Settings screen for local Jira and LLM configuration."""

import streamlit as st

from config_store import load_config, save_config


st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("Settings")
config = load_config()

with st.form("settings_form"):
    jira_url = st.text_input("Jira URL", value=config["jira_url"], placeholder="https://company.atlassian.net")
    jira_email = st.text_input("Jira email ID", value=config["jira_email"])
    jira_api_token = st.text_input("Jira API token", value=config["jira_api_token"], type="password")
    provider = st.radio("LLM provider", ["Ollama", "Groq"], index=0 if config["llm_provider"] == "Ollama" else 1)
    groq_api_key = st.text_input("Groq API key", value=config["groq_api_key"], type="password")
    submitted = st.form_submit_button("Save settings", type="primary")

if submitted:
    save_config({
        "jira_url": jira_url.strip(),
        "jira_email": jira_email.strip(),
        "jira_api_token": jira_api_token,
        "llm_provider": provider,
        "groq_api_key": groq_api_key,
    })
    st.success("Settings saved locally.")

st.info("Ollama uses the local llama3.2:latest model. Groq is used only when selected or when Ollama is unavailable.")
