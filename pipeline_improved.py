import pandas as pd
import numpy as np
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
import spacy
from spacy.cli import download as spacy_download
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import umap
import plotly.express as px
from datetime import timedelta

# —— CONFIGURATION —— 
SAMPLE_SIZE        = 100
BATCH_SIZE         = 16
EMBED_MODEL        = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
SIM_THRESH         = 0.6            # cosine similarity threshold
TIME_WINDOW_DAYS   = 3              # ± days for event window
ENTITY_LABELS      = {"PERSON","ORG","GPE","LOC"}

# Postgres credentials
USER     = "postgres"
PASSWORD = quote_plus("4b.3O_XD?C9")
HOST     = "18.162.51.182"
PORT     = 5432
DBNAME   = "mydb"
DB_URL   = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

# —— LOAD DATA ——
engine = create_engine(DB_URL)
query = f"""
    SELECT id, title, content_en, published_at
    FROM news
    WHERE content_en IS NOT NULL
    ORDER BY published_at DESC NULLS LAST
    LIMIT {SAMPLE_SIZE}
"""
df = pd.read_sql(query, engine, parse_dates=["published_at"])
print(f"✅ Loaded {len(df)} articles")

# —— EMBEDDING: handle long texts by chunking ——
embedder = SentenceTransformer(EMBED_MODEL)

def embed_long_text(text, max_tokens=512):
    sentences = text.replace("\n", " ").split(". ")
    chunks, curr = [], ""
    for sent in sentences:
        if len(curr.split()) + len(sent.split()) <= max_tokens:
            curr += sent + ". "
        else:
            chunks.append(embedder.encode(curr, show_progress_bar=False))
            curr = sent + ". "
    if curr:
        chunks.append(embedder.encode(curr, show_progress_bar=False))
    return np.mean(chunks, axis=0)

print("🔢 Embedding articles...")
df["embedding"] = df["content_en"].apply(embed_long_text)
corpus_embeddings = np.vstack(df["embedding"].values)

# —— NAMED ENTITY RECOGNITION ——
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Model en_core_web_sm not found. Downloading...")
    spacy_download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

print("🗂 Extracting named entities...")
doc_ents = []
for doc in nlp.pipe(df["content_en"], batch_size= BATCH_SIZE, disable=["parser"]):
    ents = {ent.text for ent in doc.ents if ent.label_ in ENTITY_LABELS}
    doc_ents.append(ents)

# —— BUILD SIMILARITY GRAPH ——
print("🔗 Building event graph...")
sim_matrix = cosine_similarity(corpus_embeddings)
time_window = timedelta(days=TIME_WINDOW_DAYS)

G = nx.Graph()
G.add_nodes_from(range(len(df)))

for i in range(len(df)):
    for j in range(i+1, len(df)):
        # Time constraint only if both dates exist
        di = df.at[i, "published_at"]
        dj = df.at[j, "published_at"]
        if pd.notna(di) and pd.notna(dj):
            if abs(di - dj) > time_window:
                continue
        # Content similarity
        if sim_matrix[i, j] < SIM_THRESH:
            continue
        # Shared entity
        if not (doc_ents[i] & doc_ents[j]):
            continue
        G.add_edge(i, j)

# —— EXTRACT CLUSTERS ——
print("🎯 Extracting clusters...")
components = list(nx.connected_components(G))
label_map = {}
for cid, comp in enumerate(components):
    for idx in comp:
        label_map[idx] = cid

# Singletons for any node not in the graph (isolated or no edges)
max_c = max(label_map.values(), default=-1)
for idx in range(len(df)):
    if idx not in label_map:
        max_c += 1
        label_map[idx] = max_c

df["cluster_id"] = df.index.map(label_map)

# —— VISUALIZE ——
print("📊 Plotting clusters with UMAP...")
reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.05)
coords = reducer.fit_transform(corpus_embeddings)
df["x"], df["y"] = coords[:, 0], coords[:, 1]
df["short_text"] = df["content_en"].str[:100] + "..."

fig = px.scatter(
    df, x="x", y="y",
    color=df["cluster_id"].astype(str),
    hover_data=["title","short_text","published_at"],
    title="Event-Based News Clustering"
)
fig.show()

print("✅ Done! Cluster IDs are in df['cluster_id'].")
