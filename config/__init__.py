"""Configuration package for Career-Sync-AI."""

from .settings import settings
from .prompts import (
    ANALYZE_JD_PROMPT,
    DRAFT_RESUME_PROMPT,
    CRITIQUE_PROMPT,
)

__all__ = [
    "settings",
    "ANALYZE_JD_PROMPT",
    "DRAFT_RESUME_PROMPT",
    "CRITIQUE_PROMPT",
]
