"""GCS-backed persistence for the RAG eval corpus and computed embeddings.

Caching embeddings in GCS avoids re-calling the (paid) Vertex AI embeddings
API every time the notebook re-runs against an unchanged corpus.
"""

import io
import json

import numpy as np
from google.cloud import storage

# Lazily-initialized, module-level singleton. storage.Client() reads local
# ADC and opens a connection pool on construction, so we only want to pay
# that cost once per notebook session rather than once per function call.
_client = None


def _get_client() -> storage.Client:
    global _client
    if _client is None:
        _client = storage.Client()
    return _client


def upload_corpus(docs: list[str], bucket_name: str, blob_path: str = "corpus/documents.json") -> str:
    """Upload the raw document corpus to GCS as JSON. Returns the gs:// URI."""
    bucket = _get_client().bucket(bucket_name)
    blob = bucket.blob(blob_path)
    # upload_from_string overwrites any existing object at this path, so
    # re-running the notebook against an edited corpus just replaces it —
    # no manual delete/versioning step needed for this small, single-writer case.
    blob.upload_from_string(json.dumps(docs), content_type="application/json")
    return f"gs://{bucket_name}/{blob_path}"


def load_or_compute_embeddings(bucket_name: str, blob_path: str, compute_fn):
    """Return embeddings from GCS if already cached there, else compute and cache them.

    `compute_fn` takes no args and returns (embeddings: np.ndarray, latency_ms: float),
    matching the signature of the notebook's `get_embeddings` call.
    """
    bucket = _get_client().bucket(bucket_name)
    blob = bucket.blob(blob_path)

    if blob.exists():
        # Cache hit: no Vertex AI call was made, so latency is genuinely 0 —
        # the caller uses this to distinguish "loaded from cache" from
        # "computed live" without a separate boolean flag.
        buf = io.BytesIO(blob.download_as_bytes())
        return np.load(buf), 0.0

    # Cache miss: compute via the caller-supplied function (this is the
    # (paid, ~500ms) Vertex AI embeddings call), then persist the result
    # as .npy bytes so the next run hits the branch above instead.
    embeddings, latency_ms = compute_fn()
    buf = io.BytesIO()
    np.save(buf, embeddings)
    buf.seek(0)
    blob.upload_from_file(buf, content_type="application/octet-stream")
    return embeddings, latency_ms
