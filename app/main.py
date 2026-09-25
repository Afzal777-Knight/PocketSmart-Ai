from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routers import auth, planners, api, pages
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db(); yield
app=FastAPI(title=settings.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(pages.router); app.include_router(auth.router); app.include_router(planners.router); app.include_router(api.router)
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/startup")
def startup(): return {"status":"ready","service":settings.app_name}
