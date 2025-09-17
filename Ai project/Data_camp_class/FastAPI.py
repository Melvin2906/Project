from fastapi import FastAPI

# initiate app
app = FastAPI()

#Handle get request to root
@app.get("/")
def root():
    return {"message": "Hello world!"}