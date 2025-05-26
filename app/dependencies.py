import logging
from uuid import uuid4

from fastapi import Query, Request, Response

logger = logging.getLogger(__name__)


async def get_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        logger.info(f"Новая сессия создана: {session_id}")
        response.set_cookie("session_id", session_id, httponly=True)
        logger.info(f"Новая сессия создана: {session_id}")
    return session_id


class Pagination:
    def __init__(self, page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=100)):
        self.page = page
        self.limit = limit
