"""Ollama generation with optional Groq fallback."""

import os

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def _ollama(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        detail = response.text.strip()
        raise requests.HTTPError(f"{error}. Ollama response: {detail}") from error
    return response.json().get("response", "").strip()


def _groq(prompt: str, api_key: str) -> str:
    if not api_key:
        raise ValueError("Groq API key is required when Groq is selected or used as fallback.")
    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate(prompt: str, config: dict) -> tuple[str, str]:
    if config.get("llm_provider") == "Groq":
        return _groq(prompt, config.get("groq_api_key", "")), "Groq"
    try:
        return _ollama(prompt), "Ollama"
    except requests.RequestException as ollama_error:
        try:
            return _groq(prompt, config.get("groq_api_key", "")), "Groq fallback"
        except Exception as groq_error:
            raise RuntimeError(
                f"Ollama is unavailable ({ollama_error}); Groq fallback failed ({groq_error})."
            ) from groq_error
