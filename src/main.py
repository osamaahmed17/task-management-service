from fastapi import FastAPI
from src.config import settings


app = FastAPI()


print(settings.ENV)
print(settings.DATABASE_URL)


@app.get("/")
async def root():
    return {"message": "Hello World"}
