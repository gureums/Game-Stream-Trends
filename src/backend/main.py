from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.test import router as test_router
from routes.stats import router as stats_router

app = FastAPI()


@app.get('/api')
async def root():
    return {"message": "Hello, FastAPI!"}
               
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router)
app.include_router(stats_router)
