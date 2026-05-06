"""
낙화검심 - FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api.endpoints import auth, characters, game, admin
from .ws.chat import router as ws_router

app = FastAPI(title="낙화검심", version="0.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(characters.router, prefix="/api")
app.include_router(game.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(ws_router, prefix="/ws")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok", "name": "낙화검심", "version": "0.5.0"}
