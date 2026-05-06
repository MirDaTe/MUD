"""
낙화검심 - FastAPI 메인 애플리케이션
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.database import engine, Base
from .api.endpoints import auth, characters, game, admin
from .ws.chat import router as ws_router

app = FastAPI(title="낙화검심", version="0.8.0")

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

# 정적 파일 서빙 (프론트엔드)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")
app.mount("/images", StaticFiles(directory=os.path.join(FRONTEND_DIR, "images")), name="images")

from starlette.responses import FileResponse

@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    from .services.respawn_service import register_monster_templates
    register_monster_templates()


@app.get("/api/health")
def health():
    return {"status": "ok", "name": "낙화검심", "version": "0.8.0"}
