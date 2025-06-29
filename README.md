# S-News
# Personalized and Statistical News Aggregator Minimum Viable Product (MVP)

**What it is:**  
This project implements the initial scaffold of S-News, featuring:

Region & Topic SelectionChoose your region and topics to personalize your news feed.

Preferences APIBackend (FastAPI) endpoints to GET/POST user preferences.

Top Stories FeedFrontend calls NewsAPI to display top headlines filtered by region and topics.

## 📁 Repository Structure

    /s-news
    ├── backend/           # FastAPI server
    │   ├── .venv/         # Python virtualenv
    │   ├── .env           # (gitignored) OPENAI_API_KEY, etc.
    │   ├── requirements.txt
    │   └── app/
    │       ├── main.py            # Application entrypoint
    │       ├── api/
    │       │   └── preferences.py # GET/POST /preferences
    │       ├── core/
    │       │   └── config.py      # Settings loader
    │       ├── schemas/
    │       │   └── models.py      # Pydantic models
    │       └── services/          # Business logic modules
    ├── frontend/          # React + Vite + Tailwind app
    │   ├── .env           # (gitignored) VITE_NEWSAPI_KEY
    │   ├── index.html
    │   ├── vite.config.js
    │   ├── package.json
    │   └── src/
    │       ├── main.jsx           # React entrypoint
    │       ├── App.jsx            # Top-level component
    │       ├── index.css          # Tailwind imports
    │       ├── contexts/          # PreferencesContext
    │       ├── components/        # Region & Topic selectors, TopStories
    │       ├── pages/             # Home page
    │       └── services/          # preferencesApi.js, newsApi.js
    └── README.md          # <-- you are here

---

### Prerequisites

- **Node.js** (v16+)
- **npm** (v8+)
- **Python 3.8+**
- **Git**

### 1. Clone the repo

```bash
git clone git@github.com:<your-username>/s-news.git
cd s-news
```
### 2. Set up backend

```bash
cd backend
# create & activate virtualenv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# (optional) configure .env
# create backend/.env with:
# OPENAI_API_KEY=<your_key>

# run the server
uvicorn app.main:app --reload
```

### 3. Setup Frontend
```bash
cd ../frontend
# install dependencies
npm install

# configure .env
# create frontend/.env with:
# VITE_NEWSAPI_KEY=<your_newsapi_key>

# run the dev server
npm run dev
```

