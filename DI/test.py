import datetime

from fastapi import FastAPI, Depends

app = FastAPI()

def get_user():
    user = {
        "name": "Vitaliy",
        "email": "Vitalya@mail.ru",
        "age": 15
    }

    user.update({
        "pet": "dog"
    })

    yield user

    print(123)

def get_uptime():
    now = datetime.datetime.now().time()
    yield now

@app.get("/")
def root(user: dict = Depends(get_user)):
    return {"user": user}