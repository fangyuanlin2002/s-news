#!/usr/bin/env python3
"""
pipeline.py

End-to-end:
  news (stored in `news.title` / `news.content`) 
    → translation 
    → embeddings 
    → UMAP 
    → HDBSCAN 
    → KeyBERT naming 
    → evaluation 
    → visualization 
    → translated_news
"""

import os
from datetime import datetime
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import (
    create_engine, text
)
from sklearn.metrics import silhouette_score, davies_bouldin_score

# NLP & ML
from transformers          import pipeline as hf_pipeline
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from keybert               import KeyBERT

# Visualization
import plotly.express as px

# —— CONFIG —— 
BATCH_SIZE       = 32
EMBED_MODEL      = "all-mpnet-base-v2"
TRANSLATE_MODEL  = "Helsinki-NLP/opus-mt-zh-en"
UMAP_KWARGS      = dict(n_components=2, n_neighbors=50, min_dist=0.1)
HDBSCAN_KWARGS   = dict(min_cluster_size=10)

# Postgres creds (URL-encode the password)
USER     = "postgres"
PASSWORD = quote_plus("4b.3O_XD?C9")
HOST     = "54.46.7.169"
PORT     = 5432
DBNAME   = "mydb"

DB_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
engine = create_engine(DB_URL, echo=False)


def load_unprocessed_news() -> pd.DataFrame:
    """
    Fetch id, title, content for every news row not yet in translated_news.
    """
    sql = """
    SELECT n.id,
           n.title,
           n.content
      FROM news AS n
 LEFT JOIN translated_news AS t
        ON t.news_id = n.id
     WHERE t.news_id IS NULL
    """
    return pd.read_sql(sql, engine)


def batch_translate(texts: list[str]) -> list[str]:
    """Translate Traditional Chinese → English in batches."""
    translator = hf_pipeline(
        "translation",
        model=TRANSLATE_MODEL,
        batch_size=BATCH_SIZE,
        device=0
    )
    outputs = translator(texts)
    return [o["translation_text"] for o in outputs]


def embed_reduce_cluster(meta_texts: list[str]):
    # 1) Embed
    embedder   = SentenceTransformer(EMBED_MODEL)
    embeddings = embedder.encode(meta_texts, show_progress_bar=True)

    # 2) UMAP → 2D
    reducer = umap.UMAP(**UMAP_KWARGS)
    proj    = reducer.fit_transform(embeddings)

    # 3) HDBSCAN
    clusterer = hdbscan.HDBSCAN(**HDBSCAN_KWARGS)
    labels    = clusterer.fit_predict(proj)

    return embeddings, proj, labels


def evaluate(emb: list[list[float]], labels: list[int]):
    mask = labels != -1
    if mask.sum() < 2:
        return None, None
    sil = silhouette_score(emb[mask], labels[mask], metric="cosine")
    db  = davies_bouldin_score(emb[mask], labels[mask])
    return sil, db


def name_clusters(df: pd.DataFrame, top_n=3) -> dict[int,str]:
    """Map each cluster ID to its top keywords."""
    kw = KeyBERT()
    mapping = {}
    for cid in sorted(df["cluster"].unique()):
        if cid == -1:
            mapping[cid] = "outliers"
            continue
        blob = " ".join(df.loc[df["cluster"] == cid, "content_en"])
        kws, _ = zip(*kw.extract_keywords(blob, top_n=10))
        # simple dedupe
        name = []
        for w in kws:
            if not any(w in ex for ex in name):
                name.append(w)
            if len(name) >= top_n:
                break
        mapping[cid] = " / ".join(name)
    return mapping


def visualize(df: pd.DataFrame, out_file="cluster_viz.html"):
    fig = px.scatter(
        df, x="x", y="y",
        color="cluster_name",
        hover_data={"title_en": True},
        template="plotly_dark",
        title="UMAP + HDBSCAN News Clusters"
    )
    fig.write_html(out_file)
    print(f"🔍 Visualization saved to {out_file}")


def upsert_translated(df: pd.DataFrame):
    """
    Upsert translated rows into translated_news, ignoring duplicates via ON CONFLICT.
    """
    now = datetime.utcnow()
    insert_sql = text("""
    INSERT INTO translated_news
      (news_id, title_en, content_en, cluster_id, cluster_name, processed_at)
    VALUES
      (:news_id, :title_en, :content_en, :cluster_id, :cluster_name, :processed_at)
    ON CONFLICT (news_id) DO NOTHING
    """)
    with engine.begin() as conn:
        for _, r in df.iterrows():
            conn.execute(insert_sql, {
                "news_id":      int(r["id"]),
                "title_en":     r["title_en"],
                "content_en":   r["content_en"],
                "cluster_id":   int(r["cluster"]),
                "cluster_name": r["cluster_name"],
                "processed_at": now
            })


def main():
    df = load_unprocessed_news()
    if df.empty:
        print("✅ No new `news` rows to process.")
        return

    # 1) Translate
    df["title_en"]   = batch_translate(df["title"].tolist())
    df["content_en"] = batch_translate(df["content"].tolist())

    # 2) Embed → UMAP → HDBSCAN
    df["meta"] = df["title_en"] + " " + df["content_en"]
    emb, proj, labels = embed_reduce_cluster(df["meta"].tolist())
    df["x"], df["y"], df["cluster"] = proj[:,0], proj[:,1], labels

    # 3) Evaluate
    sil, db = evaluate(emb, labels)
    print(f"✨ Silhouette (no outliers): {sil:.3f}")
    print(f"✨ Davies–Bouldin index: {db:.3f}")

    # 4) Name clusters
    mapping = name_clusters(df)
    df["cluster_name"] = df["cluster"].map(mapping)

    # 5) Visualize
    visualize(df)

    # 6) Persist
    upsert_translated(df)
    print("✅ Pipeline complete.")


if __name__ == "__main__":
    main()
