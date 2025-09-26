from fastapi import FastAPI

# initiate app
app = FastAPI()

#Handle get request to root
@app.get("/")
def root():
    return {"message": "Hello world!"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define model Item
class Item(BaseModel):
    name: str
    description: str

# Define items at application start
items = {"bananas": "Yellow fruit."}

app = FastAPI()


@app.put("/items")
def update_item(item: Item):
    name = item.name
    # Update the description
    items[name] = item.description
    return item


class Item_(BaseModel):
    name: str

# Define items at application start
items = {"apples", "oranges", "bananas"}

app = FastAPI()
items = {"apples", "oranges"}

@app.delete("/items")
def delete_item(item: Item_):
    name = item.name
    if item.name not in items:
        raise HTTPException(status_code=404, detail="Item not found.")
    else:
    # Delete the item
        items.remove(name)
        return {}


# Informational responses (100 - 199)
# Successful responses (200 - 299):
    # 200 = Ok
    # 201 = Created
    # 202 = Accepted
    # 204 = No content
# Redirection messages (300 - 399):
    # 301 = Moved Permantently
# Client error responses (400 - 499):
    # 400 = Bad request
    # 404 = Not found
# Server error responses (500 - 599):
    # 500 = Internal serveur error

def some_library():
    return

@app.get("/")
async def read_results():
    results = await some_library()
    return results



# Define model Item
class _Item_(BaseModel):
    name: str

app = FastAPI()

items = {"rock", "paper", "scissors"}


@app.delete("/items")
# Make asynchronous
async def root(item: _Item_):
    name = item.name
    # Check if name is in items
    if name not in items:
        # Return the status code for not found
        raise HTTPException(status_code=404, detail="Item not found.")
    items.remove(name)
    return {"message": "Item deleted"}

def main():
    print("Hello")
# Unit tests
def test_main():
    response = main()
    assert response == {"msg": "Hello"}

#Import TestClient and app

from fastapi.testclient import TestClient
from .FastAPI import app

# Create test client with application context
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello"}

# Functional Tests
def test_delete_then_read():
    response = client.delete("/items/1")
    assert response.status_code == 200
    response = client.get("/items/1")
    assert response.status_code == 404