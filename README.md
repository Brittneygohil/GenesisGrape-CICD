# 🍷 GenesisGrape — Streamlit App with CI/CD on Google Cloud Run  

## 📖 Overview  
GenesisGrape is a **Streamlit-based wine recommender app** that analyzes wine data to help beginners discover affordable and beginner-friendly wines.  
In this project, a **full CI/CD pipeline** was implemented using **Google Cloud Build**, **Artifact Registry**, and **Cloud Run**, enabling automatic deployment whenever new commits are pushed to GitHub.  

---

## 🚀 Features  
- **End-to-End CI/CD Pipeline:** Automated build, test, and deploy workflow on Google Cloud.  
- **Containerization:** Dockerized Streamlit app for consistent environment and reproducible builds.  
- **Serverless Deployment:** Runs on Google Cloud Run with HTTPS and auto-scaling.  
- **Artifact Management:** Stores container images securely in Google Artifact Registry.  
- **Zero Manual Steps:** Full automation triggered from GitHub commits.  

---

## 🧰 Tech Stack  
| Category | Tools |
|-----------|--------|
| Language | Python 3.11 |
| Framework | Streamlit |
| CI/CD | Google Cloud Build |
| Deployment | Google Cloud Run |
| Containerization | Docker |
| Registry | Artifact Registry |

---

## ⚙️ CI/CD Pipeline Flow  
1. **Code Commit** → GitHub main branch.  
2. **Cloud Build Trigger** executes automatically.  
3. **Docker Image** built using `Dockerfile`.  
4. **Image Pushed** to Artifact Registry.  
5. **App Deployed** to Cloud Run (region: `us-central1`).  

---



