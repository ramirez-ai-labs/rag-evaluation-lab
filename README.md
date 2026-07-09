# 🧪 RAG Evaluation Lab (Beginner-Friendly Guide)

Welcome to the **RAG Evaluation Lab**! This project is a simple, beginner-friendly introduction to how we evaluate **Retrieval-Augmented Generation (RAG)** systems—the same technique used in modern AI assistants, documentation bots, and advanced search tools.

This lab helps you understand:

- What RAG is  
- Why RAG systems need evaluation  
- How to compute simple retrieval metrics like Recall@k and Precision@k  
- How to compare a keyword baseline with TF-IDF retrieval  
- How to use a simple answer-overlap score as a first check on answer quality  

Everything is built to be **easy**, **hands-on**, and **self-contained**.

---

## 🧠 What Is RAG?

**Retrieval-Augmented Generation (RAG)** is a method where an AI model is given extra information from a document store *before* answering a question.

Think of it like an LLM saying:

> “Hold on — let me look that up first.”

A RAG pipeline has two main components:

1. **Retriever** – Finds the most relevant documents  
2. **Generator** – Produces an answer using those documents  

This lab focuses on **measuring how well that process works**.

---

## 🎯 Why Evaluate RAG?

A RAG system can fail in multiple ways:

- It retrieves the wrong documents  
- It retrieves irrelevant or noisy text  
- It retrieves too slowly  
- It generates answers not grounded in the retrieved content  

To improve a RAG system, we need to **measure**:

- How well retrieval works  
- How accurate generated answers are  
- How the whole system behaves end-to-end  

That’s what this evaluation lab teaches.

---

## 📊 What This Beginner Lab Covers

This repo stays intentionally small and focuses on the foundations:

### **1️⃣ Retrieval Evaluation**  
“Did we find the correct documents?”

The notebook teaches:

- **Recall@k** — How much of the relevant information appears in the top results  
- **Precision@k** — How clean or relevant the returned top results are  
- A comparison between a simple **keyword overlap retriever** and a **TF-IDF + cosine similarity** retriever  

### **2️⃣ Basic Answer Evaluation**  
“Did the answer use the important ideas from the reference answer?”

The notebook includes:

- A small set of **gold answers**  
- A small set of **model answers**  
- A **simple overlap score** based on important words after light normalization  

### **3️⃣ Next-Step Ideas**  
Once the basics make sense, you can extend this notebook with:

- **MRR** or other ranking metrics  
- Embedding-based retrieval  
- LLM-as-a-judge scoring  
- Latency and cost tracking  

---

## 🧩 What’s Inside This Lab?

The lab includes:

- **A small synthetic corpus** of developer-focused documents  
- **Ground-truth relevance labels** for each query  
- A **keyword-overlap retriever**  
- A **TF-IDF + cosine similarity retriever**  
- **Retrieval metrics** (Recall@k and Precision@k)  
- A **simple answer-overlap metric** for beginner-friendly answer evaluation  

It is intentionally small so you can understand each step clearly.

---

## 🏗️ Project Structure

```bash
rag-evaluation-lab/
│
├── rag_evaluation_lab.ipynb      # Part 1 — beginner notebook (keyword vs TF-IDF)
├── rag_evaluation_vertex.ipynb   # Part 2 — Vertex AI Embeddings benchmark; Part 3 adds BigQuery
├── lib/
│   ├── gcs_utils.py              # Cloud Storage: corpus upload + embedding cache (Phase 1)
│   └── bq_writer.py              # BigQuery: persist benchmark results for querying (Phase 3)
├── tests/
│   └── test_gcs_utils.py         # Mocked unit tests for lib/gcs_utils.py (no GCP calls)
├── requirements.txt              # Pinned dependencies (Vertex AI, Cloud Storage, BigQuery)
├── retrieval_benchmark_vertex.png
└── README.md                     # This guide
```

---

## 🚀 How to Run the Lab

1. **Install dependencies**

   ```bash
   pip install numpy pandas scikit-learn matplotlib jupyter
   ```

2. **Launch the notebook**

   ```bash
   jupyter notebook rag_evaluation_lab.ipynb
   ```

3. **Run each cell step-by-step**

   You will see:

   - A tiny synthetic corpus  
   - Retrieval results  
   - Recall@k and Precision@k  
   - A keyword vs TF-IDF comparison  
   - A simple answer-overlap score  

---

## ⭐ What You Will Learn

By completing this lab, you will understand:

- How RAG systems retrieve documents  
- How a simple keyword baseline differs from TF-IDF retrieval  
- How to measure retrieval accuracy  
- How to think about answer quality with lightweight metrics  

This gives you a strong foundation for evaluating larger or production RAG pipelines.

---

## 🧠 Suggested Next Steps

Here are ways to extend the lab:

- Experiment with different chunk sizes  
- Add latency measurement  
- Add more complex question types  
- Use real documentation instead of synthetic text  

For MRR and embedding-based retrieval, see **Part 2** below.

---

## 🚀 Part 2 — Vertex AI Embeddings Benchmark (Production-Ready)

`rag_evaluation_vertex.ipynb` extends the lab with Google's `text-embedding-004` model via
Vertex AI, benchmarking embedding-based retrieval against the keyword and TF-IDF baselines
from Part 1 across **Recall@k**, **Precision@k**, **MRR**, **latency**, and **cost**.

It reuses the exact same synthetic corpus, ground-truth labels, and metric functions as
Part 1 — only the retriever changes — so the comparison is apples-to-apples. Part 1 stays
untouched as the standalone beginner baseline.

### What You'll Learn in Part 2

Beyond retrieval quality metrics, Part 2 adds **production considerations**:

- **Latency** – How fast does each retriever respond? (Keyword/TF-IDF: 1–5ms, Vertex AI embeddings: 50–200ms)
- **Cost** – What's the per-query cost at scale? (Keyword/TF-IDF: ~$0, Vertex AI: $20–100 per 1M queries)
- **Trade-off Framework** – When would you recommend embeddings over TF-IDF to a customer? (Quality vs. cost vs. speed)

This is exactly how a production RAG consultant (Forward Deployed Engineer) thinks: **"Embeddings improve recall by 15%, but cost $500/month. Is that worth it for your use case?"**

The notebook includes a decision tree for common scenarios:
- Need results in 2 weeks? → Keyword or TF-IDF (no setup)
- Have a GCP project and can wait? → Embeddings (best quality)
- 10M+ documents? → Consider Vertex AI Search (managed service)

### GCP Setup

You need a Google account and a GCP project with billing enabled (a card on file is
required even for free-tier usage — you won't be charged for this lab; embedding calls on
this tiny corpus cost effectively $0, and new accounts get $300 in free credits).

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a project (e.g. `ramirez-rag-lab`)
2. Enable billing on that project, and set a budget alert ($1–5) as a tripwire
3. Enable the Vertex AI, BigQuery, and Cloud Storage APIs:

   ```bash
   gcloud services enable aiplatform.googleapis.com bigquery.googleapis.com storage.googleapis.com
   ```

4. Authenticate locally:

   ```bash
   gcloud auth application-default login
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   ```

5. Create the Cloud Storage bucket used to cache the corpus and embeddings (Part 2 writes
   here so re-running the notebook doesn't re-call the paid embeddings API for an unchanged
   corpus — see `lib/gcs_utils.py`):

   ```bash
   gcloud storage buckets create gs://rag-eval-lab-YOUR_PROJECT_ID \
     --project=YOUR_PROJECT_ID --location=us-central1 --uniform-bucket-level-access
   ```

6. Install dependencies and run the notebook:

   ```bash
   pip install -r requirements.txt
   jupyter notebook rag_evaluation_vertex.ipynb
   ```

7. Set `GCP_PROJECT_ID` and `GCS_BUCKET_NAME` in the notebook's config cell to match your project and bucket.

Full step-by-step setup commands (including the BigQuery piece landing next) are tracked in
[`plan.md`](./plan.md).

---

## 🗄️ Part 3 — Cloud Persistence Layer (BigQuery + Cloud Storage)

Parts 1 and 2 run entirely in notebook memory — the benchmark results exist only until you
close the kernel. Part 3 adds **production-grade persistence** so you can:

- **Query benchmark history** across runs without re-running notebooks
- **Compare retrievers** over time (e.g., "Did embeddings improve after retraining?")
- **Track cost vs. quality trade-offs** with queryable metrics

### What Part 3 Adds

Two Google Cloud services, both under their always-free tiers:

**Cloud Storage (Phase 1 — already live)**
- **Why**: Cache the corpus and computed embeddings so re-running the notebook doesn't re-call the paid Vertex AI API
- **How**: `lib/gcs_utils.py` checks GCS before recomputing; writes go to `gs://rag-eval-lab-YOUR_PROJECT_ID/corpus/` and `/embeddings/vertex/`
- **Cost**: <1 MB per run, well under the 5 GB always-free tier → **$0 expected**

**BigQuery (Phase 3 — new)**
- **Why**: Store benchmark results (Recall@k, Precision@k, MRR, latency, cost) as queryable rows
- **How**: After each run, `lib/bq_writer.py` writes results to `rag_eval_lab.benchmark_runs` table
- **Query example**: `SELECT retriever_type, AVG(recall_at_k), AVG(latency_ms) FROM benchmark_runs GROUP BY retriever_type` — no re-running needed
- **Cost**: <1 MB processed per run, well under the 1 TB/month always-free tier → **$0 expected**

### Production Pattern: Cache + Query

This mirrors how real RAG teams operate:

1. **Run notebook** → Compute embeddings, store in GCS, benchmark retrievers
2. **Write results** → BigQuery row per run
3. **Query history** → Compare performance across corpus sizes, models, or time
4. **Decide**: "Embeddings improved recall 15%, but now cost $500/month. Worth it?"

The notebook includes a sample SQL query showing aggregated metrics across all past runs.

### No Code Changes Needed

If you have Part 2 running, Part 3 is automatic:

- The notebook cells handle data prep and BigQuery writes
- Results persist after each run
- The sample query is pre-built and executed

---

### Running the Tests

`lib/gcs_utils.py` has a mocked unit test suite — no GCP credentials or network calls:

```bash
python -m unittest tests.test_gcs_utils -v
```

Happy building!
