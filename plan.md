# Plan: BigQuery + Cloud Storage Integration for rag-evaluation-lab

Extends Part 2 (`rag_evaluation_vertex.ipynb`) by persisting benchmark results to BigQuery and moving the corpus/embeddings to Cloud Storage. Goal: demonstrate working, cost-aware integrations with Vertex AI, BigQuery, and Cloud Storage in one artifact. Estimated effort: half a day, split across independently shippable phases.

## Phase 0 — GCP setup (~15 min, one-time) — ✅ DONE

- [x] Attach a billing account to the existing Vertex AI project (card on file, $0 expected spend).
- [x] Set a budget alert ($1–5) on the billing account as a tripwire against runaway/looped API calls.
- [x] Enable APIs: `bigquery.googleapis.com`, `storage.googleapis.com`.
- [x] Create one GCS bucket in `us-central1` (required region for Always Free tier): `gs://rag-eval-lab-ramirez-rag-lab/`.
- [x] Create one BigQuery dataset: `rag_eval_lab` (location `US`, matches on-demand free tier) — project `ramirez-rag-lab`.
- [x] ~~Scope IAM narrowly~~ — skipped: sole identity is the project owner's own user ADC, not a separate service account, so per-role scoping doesn't apply here.
- [x] Confirm auth path is Application Default Credentials (`gcloud auth application-default login` + `set-quota-project ramirez-rag-lab`), consistent with the existing Vertex AI setup in Part 2. No service-account JSON keys committed to the repo.
- [x] Add a `.gitignore` rule for any credential/key file as a backstop (`*service-account*.json`, `*credentials*.json`, `gcp-key*.json`).

Infrastructure is live: project `ramirez-rag-lab`, bucket `gs://rag-eval-lab-ramirez-rag-lab`, dataset `ramirez-rag-lab:rag_eval_lab`. Phase 1/2 can start.

## Phase 1 — Cloud Storage: corpus + embeddings persistence (~1.5 hrs) — ✅ DONE (pending your local run)

Goal: move the synthetic corpus and computed embeddings from local/in-notebook state to GCS, demonstrating a real storage-tier decision.

- [x] Bucket structure: `gs://rag-eval-lab-ramirez-rag-lab/corpus/` (raw docs), `gs://rag-eval-lab-ramirez-rag-lab/embeddings/vertex/text-embedding-004/` (serialized `text-embedding-004` vectors as `.npy`).
- [x] New module `lib/gcs_utils.py`:
  - `upload_corpus(docs, bucket)`
  - `load_or_compute_embeddings(bucket, path, compute_fn)` — checks GCS before re-calling the Vertex AI embeddings API, avoiding redundant paid calls.
- [x] Updated `rag_evaluation_vertex.ipynb`: corpus upload + GCS-backed embedding cache wired into Section 3.5, replacing the direct `get_embeddings()` call for `doc_embeddings`. Part 1/Part 2 retrieval logic untouched — only the storage layer changed. Query-time embeddings stay uncached (correctly — only the corpus is stable/cacheable).
- [ ] Verify cost: `gcloud storage du -s gs://rag-eval-lab-ramirez-rag-lab/` after a run, confirm well under 5 GB. **Not yet run** — this Mac has no `jupyter`/GCP credentials configured (the notebook was previously run from a different machine per its output logs); run the notebook top-to-bottom on your usual machine to confirm end-to-end and check this box.

## Phase 2 — BigQuery: benchmark results as a queryable table (~2 hrs)

Goal: every benchmark run (Recall@k, Precision@k, MRR, latency, cost, per retriever type) lands as rows in BigQuery instead of a DataFrame that dies with the kernel.

- [ ] Schema for `rag_eval_lab.benchmark_runs`: `run_id, timestamp, retriever_type (keyword/tfidf/vertex_embeddings), recall_at_k, precision_at_k, mrr, latency_ms, estimated_cost_usd, corpus_size, k_value`.
- [ ] New module `bq_writer.py`: `write_benchmark_results(df, table_id)` using `google-cloud-bigquery`'s `load_table_from_dataframe` (or `pandas-gbq`). Sink only, no pipeline logic.
- [ ] Notebook change: final cell of Part 2 (or new Part 3 cell) calls `write_benchmark_results()` after computing metrics. Keep existing local CSV/plot output — BigQuery is additive.
- [ ] Add one real query cell, executed against actual rows, output kept in the committed notebook (not left to run on demand):

  ```sql
  SELECT retriever_type, AVG(recall_at_k), AVG(latency_ms)
  FROM rag_eval_lab.benchmark_runs
  GROUP BY retriever_type
  ```

- [ ] Verify cost: dry-run the query (`dry_run=True`) to confirm bytes processed is near-zero.

## Phase 3 — Documentation (~30 min)

- [ ] Add a "Part 3: Cloud Persistence Layer" section to the README, matching the existing Part 2 voice:
  - Why BigQuery for results (queryable history across runs, no re-running notebooks to compare) vs. why GCS for embeddings (avoid recomputation cost/latency on Vertex AI calls).
  - Extend the existing decision-tree framing: *"Need to compare past benchmark runs? → BigQuery. Need to avoid re-embedding the same corpus? → GCS cache."*
  - Explicit cost line: "BigQuery: <1 MB processed per run, well under the 1 TB/month always-free tier. Cloud Storage: <1 MB stored, well under the 5 GB always-free tier. Billing account required; $0 expected spend, budget alert configured."
- [ ] Update the top-of-README summary line to mention BigQuery + Cloud Storage alongside Vertex AI Embeddings.

## Sequencing

BigQuery (Phase 2) before Cloud Storage (Phase 1) if shipping incrementally — it's the more directly named qualification and the query-example cell is the highest-signal single addition. Both phases are independent of each other and only depend on Phase 0.

## Gap closure

| Preferred qualification item | Before | After |
| --- | --- | --- |
| Vertex AI | closed | closed |
| BigQuery | open | closed |
| Cloud Storage | open | closed |
| Dialogflow | open | open (separate decision, out of scope for this plan) |
