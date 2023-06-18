import psycopg2
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class DatabaseErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except psycopg2.OperationalError as e:
            if 'database' in str(e) and 'does not exist' in str(e):
                return JSONResponse({"detail": "Invalid UUID was given!"}, status_code=400)
            else:
                raise e
