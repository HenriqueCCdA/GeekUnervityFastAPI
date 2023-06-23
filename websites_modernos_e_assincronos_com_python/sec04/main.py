from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from views import home_view

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(home_view.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

if __name__  == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
