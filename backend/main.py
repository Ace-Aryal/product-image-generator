# def main():
#     print("Hello from backend!")


# if __name__ == "__main__":
#     main()
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from backend!"}
