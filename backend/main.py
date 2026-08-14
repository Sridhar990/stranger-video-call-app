from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.users import router as users_router

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
app.include_router(users_router)


