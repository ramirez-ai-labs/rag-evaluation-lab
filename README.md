# 🧪 RAG Evaluation Lab (Beginner-Friendly Guide)

Welcome to the **RAG Evaluation Lab**! This project is a simple, beginner-friendly introduction to how we evaluate **Retrieval-Augmented Generation (RAG)** systems—the same technique used in modern AI assistants, documentation bots, and advanced search tools.

This lab helps you understand:

- What RAG is  
- Why RAG systems need evaluation  
- The three main types of RAG evaluation  
- How to compute simple retrieval metrics (Recall@k, Precision@k, MRR)  
- Optional LLM answer generation  
- Optional LLM-as-judge scoring  

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

## 📊 The Three Parts of RAG Evaluation

This project covers the three pillars of RAG evaluation:

### **1️⃣ Retrieval Evaluation**  
“Did we find the correct documents?”

We measure:

- **Recall@k** — Did any relevant doc appear in the top-k results?  
- **Precision@k** — Of the retrieved docs, how many were relevant?  
- **MRR (Mean Reciprocal Rank)** — How high the first relevant doc appears  

These metrics help choose:

- The best **embedding model**  
- The best **chunk size**  
- The optimal **top-k** value  

### **2️⃣ Generation Evaluation** *(optional)*  
“Did the LLM produce a correct answer?”

You can evaluate:

- Correctness  
- Faithfulness (is the answer grounded in retrieved text?)  
- Whether the answer hallucinates  

This lab includes optional support for:

- LLM-generated answers  
- LLM-as-judge evaluation  

### **3️⃣ End-to-End Evaluation** *(optional)*  
“How well does the entire RAG pipeline work?”

Optional evaluations include:

- End-to-end accuracy  
- Latency  
- Error patterns  
- Cost per query  

---

## 🧩 What’s Inside This Lab?

The lab includes:

- **A small synthetic corpus** of developer-focused documents  
- **Ground-truth Q&A pairs** mapping questions to relevant documents  
- **Embeddings + vector search** to simulate retrieval  
- **Retrieval metrics** (Recall@k, Precision@k, MRR)  
- Optional components:
  - **LLM answer generation**
  - **LLM-as-judge scoring**

It is intentionally small so you can understand each step clearly.

---

## 🏗️ Project Structure

```bash
rag-evaluation-lab/
│
├── notebooks/
│   └── rag_evaluation_lab.ipynb  # Main evaluation notebook
│
├── data/
│   ├── documents.json            # Synthetic documents
│   └── qa_pairs.json             # Ground-truth Q&A
│
├── README.md                     # Beginner-friendly guide
│
└── utils/                        # Optional helper functions
```

---

## 🚀 How to Run the Lab

1. **Install dependencies**

   ```bash
   pip install sentence-transformers numpy pandas scikit-learn matplotlib
   ```

2. **Launch the notebook**

   ```bash
   jupyter notebook notebooks/rag_evaluation_lab.ipynb
   ```

3. **Run each cell step-by-step**

   You will see:

   - Document embeddings  
   - Retrieval results  
   - Retrieval metrics  
   - Optional generation  
   - Optional judging  

---

## ⭐ What You Will Learn

By completing this lab, you will understand:

- How RAG systems retrieve documents  
- How embeddings and vector search work  
- How to measure retrieval accuracy  
- How to think about generation correctness  
- How LLMs can be used as evaluation judges  

This gives you a strong foundation for evaluating larger or production RAG pipelines.

---

## 🧠 Suggested Next Steps

Here are ways to extend the lab:

- Compare multiple embedding models  
- Experiment with different chunk sizes  
- Plot retrieval metrics as charts  
- Add latency measurement  
- Add more complex question types  
- Use real documentation instead of synthetic text  

Happy building!
