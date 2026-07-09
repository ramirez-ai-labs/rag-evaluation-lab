"""BigQuery persistence for RAG evaluation benchmark results.

Writes benchmark metrics (Recall@k, Precision@k, MRR, latency, cost) as rows
in BigQuery so they're queryable across runs without re-running notebooks.
"""

import uuid
from datetime import datetime

import pandas as pd
from google.cloud import bigquery


def write_benchmark_results(
    df: pd.DataFrame,
    table_id: str,
    run_id: str | None = None,
) -> str:
    """Write benchmark results DataFrame to BigQuery.

    Args:
        df: DataFrame with columns [retriever_type, recall_at_k, precision_at_k,
            mrr, latency_ms, estimated_cost_usd, corpus_size, k_value].
        table_id: BigQuery table ID in format "project.dataset.table".
        run_id: Unique run identifier (auto-generated if None).

    Returns:
        The run_id that was written.
    """
    if run_id is None:
        run_id = str(uuid.uuid4())

    client = bigquery.Client()

    # Add metadata columns to each row
    df = df.copy()
    df["run_id"] = run_id
    df["timestamp"] = datetime.utcnow().isoformat()

    # Preserve column order: metadata first, then metrics
    df = df[
        [
            "run_id",
            "timestamp",
            "retriever_type",
            "recall_at_k",
            "precision_at_k",
            "mrr",
            "latency_ms",
            "estimated_cost_usd",
            "corpus_size",
            "k_value",
        ]
    ]

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f"Wrote {len(df)} benchmark results to {table_id} (run_id={run_id})")
    return run_id
