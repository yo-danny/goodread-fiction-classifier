from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.predict import Predictor
from src.data_collector import fetch_book_description

app = FastAPI()
predictor = Predictor()


class Request(BaseModel):
    url: str


@app.get("/")
def home():
    return {"message": "Goodreads classifier API is running"}


@app.post("/predict")
def predict(req: Request):
    description = fetch_book_description(req.url)

    if not description:
        raise HTTPException(
            status_code=400, detail="Could not extract book description"
        )

    result = predictor.predict_from_text(description)

    return {"url": req.url, "description_preview": description[:200], **result}
