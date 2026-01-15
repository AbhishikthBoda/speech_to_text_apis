from fastapi import FastAPI
from app.stt import router as stt_router
from app.tts import router as tts_router

app = FastAPI(title="Voice Service")

app.include_router(stt_router, prefix="/stt")
app.include_router(tts_router, prefix="/tts")

@app.get("/health")
def health():
    return {"status": "ok"}
