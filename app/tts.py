import os
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

if not ELEVEN_API_KEY or not VOICE_ID:
    raise RuntimeError("ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID not set")


@router.post("/")
def text_to_speech(payload: dict):
    text = payload.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    url = f"https://api.in.residency.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    body = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
    }

    resp = requests.post(url, headers=headers, json=body, stream=True)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    def audio_stream():
        for chunk in resp.iter_content(chunk_size=4096):
            if chunk:
                yield chunk

    return StreamingResponse(
        audio_stream(),
        media_type="audio/mpeg",
        headers={
            # Optional but helpful
            "Content-Disposition": "inline; filename=speech.mp3"
        },
    )
