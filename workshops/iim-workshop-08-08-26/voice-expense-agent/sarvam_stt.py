"""Sarvam speech-to-text adapter. Kept separate from the graph for testability."""
from __future__ import annotations

import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"), override=True)

def transcribe(audio_bytes: bytes, filename: str, content_type: str | None = None) -> dict:
    key = os.getenv("SARVAM_API_KEY")
    if not key:
        raise RuntimeError("SARVAM_API_KEY is not configured.")
    if not audio_bytes:
        raise RuntimeError("The browser did not provide any audio data.")

    # Chrome's MediaRecorder reports values such as `audio/webm;codecs=opus`.
    # Sarvam accepts WebM, but expects the MIME type without browser codec
    # parameters in the multipart file part.
    mime_type = (content_type or "audio/webm").split(";", 1)[0].strip().lower()

    response = requests.post(
        "https://api.sarvam.ai/speech-to-text",
        headers={"api-subscription-key": key},
        files={"file": (filename, audio_bytes, mime_type)},
        # Translate makes Hindi / Tamil / Hinglish speech available to the rest
        # of the graph as English text. Keep the raw audio local in the browser.
        data={
            "model": "saaras:v3",
            "mode": os.getenv("SARVAM_STT_MODE", "translate"),
            "language_code": "unknown",
        },
        timeout=45,
    )
    if not response.ok:
        detail = response.text.strip()[:500] or "No response detail returned."
        raise RuntimeError(f"Sarvam returned HTTP {response.status_code}: {detail}")
    payload = response.json()
    return {"transcript": payload.get("transcript", ""), "request_id": payload.get("request_id")}
