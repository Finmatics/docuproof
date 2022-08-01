from functools import wraps
from typing import Any

from sanic.request import Request
from sanic.views import HTTPMethodView

from docuproof.config import Config
from docuproof.exceptions import HttpUnauthorized


def token_required(wrapped: Any) -> Any:
    def _decorator(func: Any) -> Any:
        @wraps(func)
        async def wrapper(view: HTTPMethodView, request: Request, *args: Any, **kwargs: Any) -> Any:
            token = request.headers.get("authorization")
            token = token.split(" ")[1] if token else None

            if token == Config.PRIVATE_ENDPOINTS_TOKEN:
                return await func(view, request, *args, **kwargs)
            else:
                raise HttpUnauthorized

        return wrapper

    return _decorator(wrapped)
