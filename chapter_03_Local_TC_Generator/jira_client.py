"""Small Jira REST API client used by the chat workflow."""

from typing import Any

import requests


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    return ""


def fetch_ticket(key: str, config: dict) -> dict:
    base_url = config.get("jira_url", "").rstrip("/")
    if not base_url or not config.get("jira_email") or not config.get("jira_api_token"):
        raise ValueError("Save Jira URL, email, and API token in Settings first.")

    response = requests.get(
        f"{base_url}/rest/api/2/issue/{key}",
        auth=(config["jira_email"], config["jira_api_token"]),
        headers={"Accept": "application/json"},
        params={"fields": "summary,description"},
        timeout=20,
    )
    if response.status_code == 404:
        raise ValueError(f"Jira ticket {key} was not found.")
    response.raise_for_status()
    payload = response.json()
    fields = payload.get("fields", {})
    acceptance = ""
    for field_name, value in fields.items():
        if "acceptance" in field_name.lower():
            acceptance = _text(value)
            break
    return {
        "key": key,
        "summary": _text(fields.get("summary")) or "Not specified",
        "description": _text(fields.get("description")) or "Not specified",
        "acceptance_criteria": acceptance or "Not specified",
    }
