from fastapi import FastAPI
from routes.route import router

app = FastAPI(docs_url=None, redoc_url=None)
    
app.include_router(router)
