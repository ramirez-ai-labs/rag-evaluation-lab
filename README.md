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
├── rag_evaluation_lab.ipynb   # Main beginner notebook
└── README.md                  # Beginner-friendly guide
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

- Add **MRR** and compare rank-sensitive retrieval quality  
- Compare multiple embedding models  
- Experiment with different chunk sizes  
- Plot retrieval metrics as charts  
- Add latency measurement  
- Add more complex question types  
- Use real documentation instead of synthetic text  

Happy building!
