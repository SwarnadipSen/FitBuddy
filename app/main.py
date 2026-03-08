from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routes import router

app = FastAPI(title="FitBuddy – AI Fitness Plan Generator")

base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")


@app.on_event("startup")
def on_startup() -> None:
	Base.metadata.create_all(bind=engine)


app.include_router(router)
