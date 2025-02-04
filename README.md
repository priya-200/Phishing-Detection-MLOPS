# 🚀 Phishing Website Detection: Industrial-Grade ML Pipeline  

## 🔥 Introduction  
Phishing attacks are a major cybersecurity threat, costing businesses millions annually. Traditional detection methods struggle against evolving attack patterns.  

This project **isn't just another phishing detection model**—it's a **fully modular, industrial-grade ML pipeline**, built for **real-world deployment** with **logs, exceptions, and FastAPI hosting**.  

---

## 📌 Key Features  
✅ **End-to-End Machine Learning Pipeline**  
✅ **Real-Time Phishing Detection with FastAPI**  
✅ **Scalable & Modular Architecture**  
✅ **Exception Handling & Logging for Debugging**  
✅ **CI/CD & Cloud-Ready Deployment**  

---

## 📥 1️⃣ Data Ingestion  
- **Data is stored in MongoDB** for structured & scalable access.  
- **Real-time phishing URL fetching** keeps the model up to date.  

## 🔄 2️⃣ Data Preprocessing & Feature Engineering  
- Extracts **domain-based, URL-based, and content-based features**.  
- Features include **HTTPS usage, WHOIS records, domain age, URL special characters, HTML patterns, etc.**  
- Uses **scikit-learn pipelines** for automation.  

## 🎯 3️⃣ Model Training & Optimization  
- Experiments with **Random Forest, XGBoost, SVM, etc.** using **MLflow tracking**.  
- **Hyperparameter tuning** ensures high accuracy.  
- Final model is serialized using **Dill**.  

## ⚡ 4️⃣ Industrial-Grade ML Pipeline  
- **Exception Handling & Logging** 📝 – No silent failures!  
- **Config-driven Architecture** 🔧 – YAML-based configurations for easy modification.  
- **Highly Scalable** 📈 – Designed for cloud and on-premise deployment.  

## 🚀 5️⃣ FastAPI-Powered Deployment  
- **Endpoints:**  
  - `/train` – Trains and updates the model with new phishing data.  
  - `/predict` – Predicts whether a given website is **safe or phishing**.  
- **FastAPI + Uvicorn** ensures high-speed real-time predictions.  

## 🌐 6️⃣ Real-World Deployment  
- **MLflow & DagsHub** for **model versioning & tracking**.  
- **Docker containerization** makes it cloud-ready.  
- **CI/CD integration** for automated updates.  

---

## 🔧 Tech Stack  
🔹 Python  
🔹 Scikit-Learn  
🔹 Pandas  
🔹 NumPy  
🔹 FastAPI  
🔹 MongoDB  
🔹 MLflow  
🔹 DagsHub  
🔹 Docker  
🔹 Uvicorn  
🔹 PyYAML  

---

## 🛠 Installation & Setup  

### 🔹 Clone the Repository  
```bash
git clone https://github.com/priya-200/Phishing-Detection-MLOPS.git
```
## Install Dependencies
```
pip install -r requirements.txt
```
## Set Up Environment Variables

Create a .env file and add:
```
MONGODB_URL=your_mongodb_connection_string
```
## Run the FastAPI Server
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
## Access API Docs

Open http://127.0.0.1:8000/docs in your browser.
Use the /predict endpoint to classify websites as phishing or safe.

## 🚀 Why This Project?
✅ Follows Industrial MLOps Standards 🚀
✅ Scalable, Real-Time Phishing Detection 🔥
✅ Cloud-Ready, CI/CD Integrated 🌍
✅ Easy API Deployment with FastAPI ⚡

Phishing attacks won’t stop—so neither should we! 🚀

###💡 Want to contribute or improve this project? Fork it & drop your suggestions! 🙌

📜 License
This project is MIT licensed.

🔗 Follow for more updates! 👇
GitHub: priya-200
LinkedIn: PriyadharshiniJayakumar

#MachineLearning #CyberSecurity #PhishingDetection #MLOps #FastAPI #AI #DataScience #TechInnovation
