from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from core.rate_limit import limiter

from routers.auth import router as auth_router
from routers.users import router as users_router

app = FastAPI(
    title="Stranger Video Call API",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def root():
    return {
        "message": "Welcome to Stranger Video Call API"
    }


app.include_router(auth_router)
app.include_router(users_router)
