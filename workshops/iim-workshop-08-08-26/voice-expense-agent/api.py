"""Small API boundary for the React workshop UI."""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from expense_agent import clear_expenses, expense_graph, recent_expenses, save_transactions
from sarvam_stt import transcribe


app = FastAPI(title="Voice Expense Ledger API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranscriptRequest(BaseModel):
    transcript: str = Field(min_length=1, max_length=5_000)


class Transaction(BaseModel):
    id: int | None = None
    amount: float = Field(gt=0)
    description: str = Field(min_length=1, max_length=240)
    category: str = Field(min_length=1, max_length=80)
    spent_on: str = Field(min_length=10, max_length=10)


class ApprovalRequest(BaseModel):
    transactions: list[Transaction] = Field(min_length=1, max_length=20)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/ledger")
def ledger() -> dict[str, Any]:
    return {"expenses": recent_expenses(12)}


@app.delete("/api/ledger")
def reset_ledger() -> dict[str, int]:
    return {"deleted": clear_expenses()}


@app.post("/api/transcribe")
async def speech_to_text(audio: UploadFile = File(...)) -> dict[str, str | None]:
    if not audio.content_type or not audio.content_type.startswith("audio/"):
        raise HTTPException(status_code=415, detail="Please upload an audio recording.")
    try:
        result = transcribe(await audio.read(), audio.filename or "voice-note.webm", audio.content_type)
        return result
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Sarvam transcription failed: {exc}") from exc


@app.post("/api/propose")
def propose(request: TranscriptRequest) -> dict[str, Any]:
    result = expense_graph.invoke({"transcript": request.transcript.strip()})
    return {
        "transcript": result["transcript"],
        "transactions": result.get("transactions", []),
        "warnings": result.get("warnings", []),
        "audit": result.get("audit", []),
        "status": result.get("status"),
    }


@app.post("/api/approve")
def approve(request: ApprovalRequest) -> dict[str, int]:
    # This endpoint is the explicit human-approval boundary: the UI has already
    # rendered the editable proposal and the user pressed Approve.
    approved = [item.model_dump(exclude={"id"}) for item in request.transactions]
    save_transactions(approved)
    return {"saved": len(approved)}
