# manage data
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from tqdm.auto import tqdm  # Optional: for progress bars

# embeddings
from sentence_transformers import SentenceTransformer

# translation
from transformers import pipeline

# dimensionality reduction
import umap

# clustering
import hdbscan

# extract keywords from texts (optional)
from keybert import KeyBERT

# visualization
import plotly.express as px

# —— CONFIG —— The most important the parameters
SAMPLE_SIZE = 100
BATCH_SIZE = 32
EMBED_MODEL = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
TRANSLATE_MODEL = "Helsinki-NLP/opus-mt-zh-en"
UMAP_KWARGS = dict(n_components=10, n_neighbors=15, min_dist=0.01)
HDBSCAN_KWARGS = dict(
    min_cluster_size=1,    # Small cluster sizes allowed
    min_samples=1,         # Higher sensitivity for density
    cluster_selection_epsilon=0.05 # Explicitly control distance for merging clusters
)


# Postgres creds
USER = "postgres"
PASSWORD = quote_plus("4b.3O_XD?C9")  # Encode special characters
HOST = "18.162.51.182"
PORT = 5432
DBNAME = "mydb"
DB_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

# Connect to database and load data
engine = create_engine(DB_URL)
query = f"""
    SELECT id, title, content_en 
    FROM news 
    WHERE content_en IS NOT NULL
    LIMIT {SAMPLE_SIZE}
"""
df = pd.read_sql(query, engine)
print(f"✅ Loaded {len(df)} articles")

# Initialize embedding model
embedder = SentenceTransformer(EMBED_MODEL)

# Embed content
print("Creating embeddings...")
corpus_embeddings = embedder.encode(df["content_en"].values, batch_size=BATCH_SIZE, show_progress_bar=True)
print(f"Embeddings shape: {corpus_embeddings.shape}")

# Dimensionality reduction with UMAP
print("Reducing dimensions with UMAP...")
reduced_embeddings = umap.UMAP(**UMAP_KWARGS).fit_transform(corpus_embeddings)
print(f"✅ Reduced embeddings shape: {reduced_embeddings.shape}")

# Clustering with HDBSCAN
print("🧩 Clustering with HDBSCAN...")
# clusterer = hdbscan.HDBSCAN(**HDBSCAN_KWARGS)
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=2,                # must be ≥ 2
    min_samples=1,                     # still allows noise points
    cluster_selection_method='leaf',   # for fine‐grained clusters
    cluster_selection_epsilon=0.0
)
labels = clusterer.fit_predict(reduced_embeddings)

df["label"] = [str(label) for label in labels]
print(f"✅ Number of clusters found: {len(set(labels)) - (1 if -1 in labels else 0)}")

# Add 2D coordinates to dataframe
df["x"] = reduced_embeddings[:, 0]
df["y"] = reduced_embeddings[:, 1]
df["text_short"] = df["content_en"].str[:100] + "..."

# Optional: Extract keywords per cluster
extract_keywords = False
if extract_keywords:
    kw_model = KeyBERT(model=embedder)
    cluster_keywords = {}
    for label in df["label"].unique():
        if label == "-1": continue  # Skip noise
        texts = df[df["label"] == label]["content_en"].tolist()
        joined_text = " ".join(texts)
        keywords = kw_model.extract_keywords(joined_text, top_n=5)
        cluster_keywords[label] = [kw[0] for kw in keywords]
    print("🗝️ Cluster keywords:", cluster_keywords)

# Visualization
print("📊 Plotting results...")
fig = px.scatter(
    df,
    x="x", y="y",
    color="label",
    hover_data=["title", "text_short"],
    title="News Article Clustering"
)
fig.show()

# Once the clustering tool is good enough, I will upsert to the database.