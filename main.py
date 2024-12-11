from fastapi import FastAPI
from routes.route import router

app = FastAPI(docs_url="/debug/docs", redoc_url=None)
    
app.include_router(router)
