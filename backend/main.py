from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from web_scraper import scrape_url_content
from text_analyzer import analyze_text_content

app = FastAPI(title="Internal Linking Tool API", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

class TextRequest(BaseModel):
    content: str

@app.get("/")
async def root():
    return {"message": "Internal Linking Tool API"}

@app.post("/api/analyze-url")
async def analyze_url(request: URLRequest):
    """
    Analyze content from a blog URL using EXA API
    """
    try:
        result = await scrape_url_content(request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/analyze-text")
async def analyze_text(request: TextRequest):
    """
    Analyze direct text content input
    """
    try:
        result = await analyze_text_content(request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
