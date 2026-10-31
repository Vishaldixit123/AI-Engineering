"""Persist local Jira and LLM settings."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
load_dotenv(BASE_DIR / ".env")

DEFAULTS = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "llm_provider": "Ollama",
    "groq_api_key": "",
}


def load_config() -> dict:
    config = DEFAULTS.copy()
    if CONFIG_PATH.exists():
        try:
            config.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass

    env_mapping = {
        "jira_url": "JIRA_URL",
        "jira_email": "JIRA_EMAIL",
        "jira_api_token": "JIRA_API_TOKEN",
        "llm_provider": "LLM_PROVIDER",
        "groq_api_key": "GROQ_API_KEY",
    }
    for key, env_key in env_mapping.items():
        if not config[key] and os.getenv(env_key):
            config[key] = os.environ[env_key]
    if config["llm_provider"] not in {"Ollama", "Groq"}:
        config["llm_provider"] = "Ollama"
    return config


def save_config(values: dict) -> None:
    config = DEFAULTS.copy()
    config.update({key: values.get(key, "") for key in DEFAULTS})
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
