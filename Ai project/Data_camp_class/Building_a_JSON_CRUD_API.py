from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class Review(BaseModel):
    movie: str
    num_starts: int
    text: str

class DbReview(BaseModel):
    movie: str
    num_starts: int
    text: str
    # Reference database ID of Reviews
    review_id: int
# CRUD = Create, Read, Update, and Delete
crud = FastAPI()

@app.post("/reviews", response_model=DbReview)
def create_review(review: Review):
    db_review = crud.create_review(review)
    #Create review in database
    return db_review

@app.get("/reviews", response_model=DbReview)
def read_review(review_id: int):
    #Read review in database
    db_review = crud.read_review(review_id)
    return db_review

@app.put("/reviews", response_model=DbReview)
def update_review(review: DbReview):
    #Update review in database
    db_review = crud.update_review(review)
    return db_review

@app.delete("/reviews", response_model=DbReview)
def delete_review(review_id: int):
    #Delete review in database
    db_review = crud.delete_review(review_id)
    return {}