from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import entry


app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search/{author_name}")
def read_author(author_name: str):
    return entry.query(author_name)
