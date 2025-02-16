import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, status
from .core.database import Base, engine
app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"detail": "Welcome to Sola Group, the server is running"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)