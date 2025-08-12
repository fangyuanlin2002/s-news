# ===== IMPORTS =====
import os
from dotenv import load_dotenv
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import plotly.express as px

# ===== CONFIGURATION =====
# Database Configuration
load_dotenv()
SYNC_DATABASE_URL=os.getenv("SYNC_DATABASE_URL")
print(f"✅ Loaded environment variables")
# Model Configuration
MODEL_CONFIG = {
    "embed_model": "sentence-transformers/multi-qa-mpnet-base-dot-v1",
    "sample_size": 100,  # Increased for better clustering
    "batch_size": 64
}

# Clustering Configuration
CLUSTERING_CONFIG = {
    # Stage 1: Coarse Clustering (Broad Topics)
    "coarse": {
        "umap": {
            "n_components": 20,
            "n_neighbors": 30,
            "min_dist": 0.15,
            "metric": "cosine"
        },
        "hdbscan": {
            "min_cluster_size": 20,
            "min_samples": 3,
            "cluster_selection_epsilon": 0.3,
            "metric": "euclidean"
        }
    },
    # Stage 2: Fine Clustering (Specific Events)
    "fine": {
        "umap": {
            "n_components": 8,
            "n_neighbors": 8,
            "min_dist": 0.05,
            "metric": "cosine"
        },
        "hdbscan": {
            "min_cluster_size": 3,
            "min_samples": 1,
            "cluster_selection_epsilon": 0.1,
            "metric": "euclidean"
        }
    }
}

# ===== DATA LOADING =====
print("🔄 Loading data from database...")
engine = create_engine(SYNC_DATABASE_URL)
query = f"""
    SELECT id, title, content_en, published_at 
    FROM news 
    WHERE content_en IS NOT NULL
    ORDER BY published_at DESC
    LIMIT {MODEL_CONFIG['sample_size']}
"""
df = pd.read_sql(query, engine)
print(f"✅ Loaded {len(df)} articles")

# ===== EMBEDDING GENERATION =====
print("\n🔮 Generating embeddings...")
embedder = SentenceTransformer(MODEL_CONFIG["embed_model"])
corpus_embeddings = embedder.encode(
    df["content_en"].values,
    batch_size=MODEL_CONFIG["batch_size"],
    show_progress_bar=True
)
print(f"📐 Embeddings shape: {corpus_embeddings.shape}")

# ===== STAGE 1: COARSE CLUSTERING =====
print("\n🌍 Stage 1: Coarse Clustering (Broad Topics)")
# Dimensionality Reduction
coarse_reducer = umap.UMAP(**CLUSTERING_CONFIG["coarse"]["umap"])
coarse_embeddings = coarse_reducer.fit_transform(corpus_embeddings)

# Clustering
coarse_clusterer = hdbscan.HDBSCAN(**CLUSTERING_CONFIG["coarse"]["hdbscan"])
coarse_labels = coarse_clusterer.fit_predict(coarse_embeddings)
df["coarse_label"] = coarse_labels

# ===== STAGE 2: FINE CLUSTERING =====
print("\n🔎 Stage 2: Fine Clustering (Specific Events)")
df["fine_label"] = "-1"  # Initialize all as noise

for coarse_id in tqdm(set(coarse_labels), desc="Processing coarse clusters"):
    if coarse_id == -1:  # Skip noise points
        continue
    
    # Get indices for current coarse cluster
    cluster_mask = (df["coarse_label"] == coarse_id)
    cluster_indices = df.index[cluster_mask]
    
    if len(cluster_indices) < 3:  # Skip very small clusters
        continue
    
    # Fine-grained processing
    fine_reducer = umap.UMAP(**CLUSTERING_CONFIG["fine"]["umap"])
    fine_embeddings = fine_reducer.fit_transform(corpus_embeddings[cluster_indices])
    
    fine_clusterer = hdbscan.HDBSCAN(**CLUSTERING_CONFIG["fine"]["hdbscan"])
    fine_labels = fine_clusterer.fit_predict(fine_embeddings)
    
    # Create composite labels
    df.loc[cluster_indices, "fine_label"] = [f"{coarse_id}_{label}" for label in fine_labels]

# ===== VISUALIZATION =====
print("\n📊 Visualizing results...")
# Use coarse coordinates for visualization
df["x"] = coarse_embeddings[:, 0]
df["y"] = coarse_embeddings[:, 1]
df["text_preview"] = df["title"] + "<br>" + df["content_en"].str[:150] + "..."

fig = px.scatter(
    df,
    x="x", y="y",
    color="fine_label",
    hover_data=["text_preview"],
    title=f"Two-Stage News Clustering (Coarse: {len(set(coarse_labels))-1}, Fine: {len(set(df['fine_label']))-1})",
    width=1200,
    height=800
)
fig.update_traces(marker=dict(size=8, opacity=0.7))
fig.show()

# ===== CLUSTER ANALYSIS =====
print("\n🔍 Cluster Statistics:")
cluster_stats = df[df["fine_label"] != "-1"].groupby("fine_label").agg({
    "id": "count",
    "title": lambda x: x.head(3).tolist(),
    "published_at": ["min", "max"]
}).sort_values(by=("id", "count"), ascending=False)

print(cluster_stats.head(10))

