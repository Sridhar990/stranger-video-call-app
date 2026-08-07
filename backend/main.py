from fastapi import FastAPI
from routers.auth import router as auth_router

app = FastAPI(
    title="Stranger Video Call API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Stranger Video Call API"
    }


app.include_router(auth_router)


