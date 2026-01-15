import os
import requests
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_STT_URL = "https://api.in.residency.elevenlabs.io/v1/speech-to-text"

@router.post("/")
async def speech_to_text(
    audio: UploadFile = File(...)
):
    if not ELEVEN_API_KEY:
        raise HTTPException(500, "Missing API key")

    files = {
        "file": (audio.filename, await audio.read(), audio.content_type),
    }

    data = {
        "model_id": "scribe_v1", 
    }

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
    }

    resp = requests.post(
        ELEVEN_STT_URL,
        headers=headers,
        files=files,
        data=data,
        timeout=30,
    )

    if resp.status_code != 200:
        raise HTTPException(400, resp.text)
    if "application/json" not in resp.headers.get("content-type", ""):
        raise HTTPException(
            502,
            f"Unexpected response type: {resp.headers.get('content-type')} | Body: {resp.text[:200]}"
        )
    result = resp.json()

    return {
        "transcript": result.get("text", ""),
        "confidence": result.get("confidence"),
    }
