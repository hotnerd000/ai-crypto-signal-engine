from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.analyze import router as analyze_router
from backend.routes.portfolio import router as portfolio_router
from backend.routes.backtest import router as backtest_router
from backend.routes.analyze import router as bot_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(portfolio_router)
app.include_router(backtest_router)
app.include_router(bot_router)