"""Optional Langfuse wiring, isolated so tracing can never block the workflow."""
from __future__ import annotations

import os


def langfuse_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def configure_langfuse() -> bool:
    """Configure Langfuse's native Python SDK without needing LiteLLM Proxy."""
    if not langfuse_enabled():
        return False
    # HOST is retained only as a legacy fallback. LANGFUSE_BASE_URL is the
    # standard setting and must win so an inherited shell HOST cannot redirect
    # this project's traces to another region.
    if os.getenv("LANGFUSE_HOST") and not os.getenv("LANGFUSE_BASE_URL"):
        os.environ["LANGFUSE_BASE_URL"] = os.environ["LANGFUSE_HOST"]
    return True
