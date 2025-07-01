from fastapi import APIRouter, HTTPException
from app.schemas.models import NewsRequest, NewsResponse, Preferences, Region, Topic

router = APIRouter()

# in-memory store for MVP
_store: Preferences | None = None

@router.get("/", response_model=Preferences)
def get_preferences():
    # default prefs if none set
    return _store or Preferences(region=Region.GLOBAL, topics=[])

@router.post("/", response_model=Preferences)
def set_preferences(prefs: Preferences):
    global _store
    _store = prefs
    return _store

@router.post("/parse-news", response_model=NewsResponse)
def parse_news_article(news: NewsRequest):
    media_name = news.media_name
    url = news.news_url

    try:
        # Dynamically get the class from the news module
        parser_class = getattr(news, media_name)
    except AttributeError:
        raise HTTPException(status_code=400, detail=f"Media class '{media_name}' not found")

    try:
        article = parser_class(url)
        return NewsResponse(title=article.title, content=article.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing article: {str(e)}")