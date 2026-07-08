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
├── rag_evaluation_vertex.ipynb   # Part 2 — Vertex AI Embeddings benchmark
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
2. Enable billing on that project
3. Enable the Vertex AI API:

   ```bash
   gcloud services enable aiplatform.googleapis.com
   ```

4. Authenticate locally:

   ```bash
   gcloud auth application-default login
   ```

5. Install the extra dependency and run the notebook:

   ```bash
   pip install google-cloud-aiplatform
   jupyter notebook rag_evaluation_vertex.ipynb
   ```

6. Set `GCP_PROJECT_ID` in the notebook's config cell to your project ID.

Happy building!
