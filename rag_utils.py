"""
rag_utils.py

Handles embedding the conditions knowledge base and retrieving the most
relevant conditions for a given user question.

Install first:
    pip install sentence-transformers numpy

This uses a small local embedding model (no API cost, runs on CPU fine
for a dataset the size of a conditions table).
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

# Adjust this import to match your actual model location
from models.models import Condition

_model = None
_condition_ids = None
_condition_texts = None
_embeddings = None


def _get_model():
    global _model
    if _model is None:
        # Small, fast, good enough for retrieval over a few hundred/thousand rows
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _to_text(value) -> str:
    """
    Safely convert any field value to plain text, whether it's a string,
    a list (e.g. symptoms stored as JSON list), or something else.
    """
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _condition_to_text(condition: Condition) -> str:
    """
    Combine the fields you want searchable into one text blob.
    Matches your actual Condition model: name, category, overview,
    symptoms (list), treatment.
    """
    parts = [
        _to_text(getattr(condition, "name", "")),
        _to_text(getattr(condition, "category", "")),
        _to_text(getattr(condition, "overview", "")),
        _to_text(getattr(condition, "symptoms", "")),
        _to_text(getattr(condition, "treatment", "")),
    ]
    return " | ".join(p for p in parts if p)


def build_index(db: Session):
    """
    Call this once at startup (or lazily on first request) to embed
    all conditions into memory. Rebuild this if conditions change.
    """
    global _condition_ids, _condition_texts, _embeddings

    conditions = db.query(Condition).all()
    _condition_ids = [c.id for c in conditions]
    _condition_texts = [_condition_to_text(c) for c in conditions]

    model = _get_model()
    _embeddings = model.encode(_condition_texts, normalize_embeddings=True)


def retrieve_relevant_conditions(query: str, db: Session, top_k: int = 3):
    """
    Returns the top_k most relevant Condition rows for a given question.
    Builds the index automatically on first call.
    """
    global _embeddings

    if _embeddings is None:
        build_index(db)

    model = _get_model()
    query_vec = model.encode([query], normalize_embeddings=True)[0]

    # Cosine similarity (embeddings are already normalized, so it's a dot product)
    scores = np.dot(_embeddings, query_vec)
    top_indices = np.argsort(scores)[::-1][:top_k]

    top_ids = [_condition_ids[i] for i in top_indices]
    results = db.query(Condition).filter(Condition.id.in_(top_ids)).all()

    # Preserve ranking order
    results.sort(key=lambda c: top_ids.index(c.id))
    return results
