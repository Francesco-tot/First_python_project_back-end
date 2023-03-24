
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "mi aplicación con FastAPI"
app.version = "0.0.1"

@app.get("/",tags = ['home'],response_class = HTMLResponse)
def message():
    return f'Hello World'