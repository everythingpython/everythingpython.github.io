"""A small, inspectable LangGraph workflow for spoken expense capture.

The graph deliberately stops before writing anything. The UI supplies the
human-approval gate, then calls save_transactions().
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import date
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from dotenv import load_dotenv
from observability import configure_langfuse, langfuse_enabled

# Workshop credentials and region live in this project's .env. Override any
# unrelated shell-level Langfuse variables so the project cannot silently send
# traces to a different region.
load_dotenv(Path(__file__).with_name(".env"), override=True)


DB_PATH = Path(__file__).with_name("expenses.db")


class ExpenseState(TypedDict, total=False):
    transcript: str
    transactions: list[dict]
    warnings: list[str]
    audit: list[str]
    status: str


CATEGORY_KEYWORDS = {
    "food": ("lunch", "dinner", "breakfast", "coffee", "restaurant", "swiggy", "zomato"),
    "transport": ("auto", "uber", "ola", "metro", "fuel", "petrol", "cab"),
    "subscriptions": ("subscription", "netflix", "spotify", "prime", "zee5", "sonyliv"),
    "shopping": ("amazon", "flipkart", "shopping"),
    "utilities": ("electricity", "wifi", "internet", "phone bill"),
}


def _amount(value: str) -> float:
    return float(value.replace(",", ""))


def _category(text: str) -> str:
    lowered = text.lower()
    for category, words in CATEGORY_KEYWORDS.items():
        if any(word in lowered for word in words):
            return category
    return "uncategorized"


def deterministic_extract(text: str) -> list[dict]:
    """Reliable no-key fallback used when the LLM is unavailable."""
    matches = list(re.finditer(r"(?:₹|rs\.?|inr)?\s*(\d[\d,]*(?:\.\d{1,2})?)", text, re.I))
    proposals: list[dict] = []
    for index, match in enumerate(matches):
        start = max(0, match.start() - 55)
        end = min(len(text), match.end() + 65)
        snippet = text[start:end].strip(" ,.-")
        proposals.append(
            {
                "id": index + 1,
                "amount": _amount(match.group(1)),
                "description": snippet,
                "category": _category(snippet),
                "spent_on": date.today().isoformat(),
            }
        )
    return proposals


def llm_extract(text: str) -> list[dict]:
    """Use LiteLLM so the provider can be swapped without changing the graph."""
    from litellm import completion

    today = date.today().isoformat()
    system = f"""Extract expense transactions from the user's spoken note.
Return JSON only, shaped exactly as {{"transactions": [...]}}. Each transaction needs:
amount (number in INR), description (short), category (food, transport, subscriptions,
shopping, utilities, health, entertainment, work, or uncategorized), and spent_on
(YYYY-MM-DD). Normalize every description and category into English, even if the user
speaks Hindi, Tamil, or Hinglish. Today is {today}; resolve relative dates such as
"yesterday" to an actual ISO date. Never return phrases such as "yesterday's date"
in spent_on. Use today's date when no date is said. Never invent an amount. A single
spoken note can contain multiple transactions."""
    model = os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": text},
    ]
    call_args = dict(
        model=model,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},
    )
    if langfuse_enabled() and configure_langfuse():
        from langfuse import get_client

        langfuse = get_client()
        with langfuse.start_as_current_observation(
            as_type="generation", name="expense-extraction", model=model
        ) as generation:
            generation.update(input=messages, metadata={"provider": "groq", "workflow": "voice-expense-agent"})
            response = completion(**call_args)
            content = response.choices[0].message.content or "{}"
            usage = getattr(response, "usage", None)
            generation.update(
                output=content,
                usage_details={
                    "input": getattr(usage, "prompt_tokens", 0) if usage else 0,
                    "output": getattr(usage, "completion_tokens", 0) if usage else 0,
                },
            )
    else:
        response = completion(**call_args)
        content = response.choices[0].message.content or "{}"
    payload = json.loads(content)
    raw_transactions = payload.get("transactions", [])
    if not isinstance(raw_transactions, list):
        raise ValueError("LLM returned an invalid transactions field")
    proposals: list[dict] = []
    for index, item in enumerate(raw_transactions):
        if not isinstance(item, dict) or "amount" not in item:
            continue
        spent_on = str(item.get("spent_on") or today)
        try:
            date.fromisoformat(spent_on)
        except ValueError:
            spent_on = today
        proposals.append(
            {
                "id": index + 1,
                "amount": float(item["amount"]),
                "description": str(item.get("description") or "Expense"),
                "category": str(item.get("category") or "uncategorized").lower(),
                "spent_on": spent_on,
            }
        )
    return proposals


def extract_expenses(state: ExpenseState) -> ExpenseState:
    text = state["transcript"].strip()
    if os.getenv("GROQ_API_KEY"):
        try:
            trace_mode = "langfuse" if langfuse_enabled() else "local_only"
            return {
                "transactions": llm_extract(text),
                "warnings": [],
                "audit": ["extract:litellm:groq", f"observability:{trace_mode}"],
            }
        except Exception as exc:
            # An agent should degrade safely rather than turn an API outage into a write.
            return {
                "transactions": deterministic_extract(text),
                "warnings": [f"LLM extraction was unavailable; used safe fallback ({type(exc).__name__})."],
                "audit": ["extract:litellm_error", "extract:deterministic_fallback"],
            }
    return {
        "transactions": deterministic_extract(text),
        "warnings": [],
        "audit": ["extract:deterministic_fallback"],
    }


def validate_proposal(state: ExpenseState) -> ExpenseState:
    warnings = list(state.get("warnings", []))
    transactions = state.get("transactions", [])
    if not transactions:
        warnings.append("No amount was found. Say an amount, for example: '₹450 for lunch'.")
    for transaction in transactions:
        if transaction["category"] == "uncategorized":
            warnings.append(f"Transaction {transaction['id']} needs a category review.")
    return {
        "warnings": warnings,
        "audit": state.get("audit", []) + ["validate:proposal_checked"],
        "status": "needs_clarification" if not transactions else "awaiting_approval",
    }


def build_graph():
    graph = StateGraph(ExpenseState)
    graph.add_node("extract", extract_expenses)
    graph.add_node("validate", validate_proposal)
    graph.add_edge(START, "extract")
    graph.add_edge("extract", "validate")
    graph.add_edge("validate", END)
    return graph.compile()


expense_graph = build_graph()


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                spent_on TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )


def recent_expenses(limit: int = 10) -> list[dict]:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


def clear_expenses() -> int:
    """Delete ledger entries and return the number removed."""
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM expenses")
        return cursor.rowcount


def save_transactions(transactions: list[dict]) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT INTO expenses (amount, description, category, spent_on, source)
               VALUES (:amount, :description, :category, :spent_on, 'voice_agent')""",
            transactions,
        )
