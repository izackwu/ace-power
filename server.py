from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import entry

html_file = "./page.html"


def get_html_page(file_path: str) -> str:
    with open(file_path, mode="r", encoding="utf8") as f:
        return f.read()

html_content = get_html_page(html_file)

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

@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/search/{author_name}")
def read_author(author_name: str):
    return entry.query(author_name)
