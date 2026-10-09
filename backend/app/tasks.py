from typing import Dict, List, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_events_from_text(text: str) -> List[Dict[str, str]]:
    """
    Basic event extraction using keyword patterns.
    Looks for temporal markers and action verbs.
    """
    events = []
    temporal_keywords = [
        "was born",
        "died",
        "founded",
        "established",
        "proclaimed",
        "revealed",
        "wrote",
        "created",
        "destroyed",
        "conquered",
    ]
    sentences = text.split(".")
    for sent in sentences:
        for keyword in temporal_keywords:
            if keyword.lower() in sent.lower():
                events.append({"text": sent.strip(), "type": "temporal_event"})
                break
    return events[:20]


def compute_text_embedding(text: str) -> Optional[List[float]]:
    """
    Compute a simple TF-IDF based embedding.
    For production, use a proper transformer model.
    """
    if not text or len(text) < 10:
        return None
    try:
        vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
        embedding = vectorizer.fit_transform([text]).toarray()[0]
        return embedding.tolist()
    except Exception:
        return None


def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two text snippets.
    Returns a score between 0 and 1.
    """
    if not text1 or not text2:
        return 0.0
    try:
        vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception:
        return 0.0


def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """
    Extract key phrases by looking at word frequencies.
    """
    if not text:
        return []
    try:
        words = text.lower().split()
        # Filter common words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is", "was", "are"
        }
        filtered = [w.strip(".,!?;:") for w in words if w.lower() not in stop_words and len(w) > 3]
        from collections import Counter
        counts = Counter(filtered)
        return [phrase for phrase, _ in counts.most_common(top_n)]
    except Exception:
        return []

