from contextvars import ContextVar
from fastapi import Request
from typing import Optional

request_context: ContextVar[Optional[Request]] = ContextVar("request_context", default=None)
