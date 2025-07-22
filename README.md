# 💼 KaaryaSetu - Job Recommendation System

KaaryaSetu is a machine learning–powered Job Recommendation System that suggests jobs based on a candidate’s **skills, qualifications, and experience** using natural language processing (NLP) techniques.

This project leverages **TF-IDF + Cosine Similarity** to match user profiles with job descriptions in the dataset. The web interface is built using **Flask**.

---

## 🔍 Features

- Job matching based on resume input (skills, qualifications)
- Recommends top job roles with high similarity
- Web-based UI using Flask
- Uses precomputed TF-IDF vectors for fast results
- Simple and extensible codebase

---


---

## ⚙️ Installation & Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Adhiksha007/KaaryaSetu.git
cd KaaryaSetu
```

### 2. Install Git LFS (only once per machine)
```bash
git lfs install
```

### 3. Pull LFS-tracked files
```bash
git lfs pull
```

### 4. Install the requirements
```bash
pip install -r requirements.txt
````

### 5. Run the app
```bash
python app.py
```
