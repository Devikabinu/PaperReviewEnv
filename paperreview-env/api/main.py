from fastapi import FastAPI
from api.routes import router
from env.environment import PaperReviewEnv

app = FastAPI(title="PaperReviewEnv API", version="1.0.0")

app.state.env = PaperReviewEnv()

app.include_router(router)
