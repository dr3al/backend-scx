from fastapi import FastAPI
application = FastAPI()

@application.get("/hello/{name}")
def hello(name: str) -> dict[str, str]:
    return {
        "message": f"Hello, {name}!"
    }

@application.get("/")
def alive():
    return {
        "message": f"I'am alive"
    }