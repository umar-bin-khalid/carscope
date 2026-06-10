from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.agent_service import CarScopeAgent
from app.models.car import Car

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    current_car_id: Optional[Union[int, str]] = None
    saved_car_ids: Optional[List[Union[int, str]]] = None
    # Full car objects passed from the frontend (Marketcheck live listings)
    current_cars_snapshot: Optional[List[Dict[str, Any]]] = None
    saved_cars_snapshot: Optional[List[Dict[str, Any]]] = None


class ToolCallRecord(BaseModel):
    tool: str
    args: Dict[str, Any]
    result_summary: str


class ChatResponse(BaseModel):
    answer: str
    tool_calls: List[ToolCallRecord] = []


@router.post("/ask", response_model=ChatResponse)
@limiter.limit("20/minute")
async def ask_question(request: Request, chat_request: ChatRequest):
    # ── Resolve current_cars from frontend snapshot ───────────────────────────
    current_cars: List[Car] = []
    if chat_request.current_cars_snapshot:
        try:
            current_cars = [Car.model_validate(c) for c in chat_request.current_cars_snapshot]
        except Exception:
            current_cars = []

    # ── Resolve current_car ───────────────────────────────────────────────────
    current_car: Optional[Car] = None
    if chat_request.current_car_id is not None:
        current_car = next(
            (c for c in current_cars if str(c.id) == str(chat_request.current_car_id)), None
        )

    # ── Resolve saved_cars from frontend snapshot ─────────────────────────────
    saved_cars: List[Car] = []
    if chat_request.saved_cars_snapshot:
        try:
            saved_cars = [Car.model_validate(c) for c in chat_request.saved_cars_snapshot]
        except Exception:
            saved_cars = []

    # ── Run agent (new instance per request for clean state isolation) ────────
    result = await CarScopeAgent().run(
        question=chat_request.question,
        current_car=current_car,
        current_cars=current_cars,
        saved_cars=saved_cars,
    )

    return ChatResponse(
        answer=result.answer,
        tool_calls=[
            ToolCallRecord(tool=tc.tool, args=tc.args, result_summary=tc.result_summary)
            for tc in result.tool_calls
        ],
    )
