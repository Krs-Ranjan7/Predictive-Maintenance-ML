# Predictive Maintenance System (Machine Learning)

A machine learning–based predictive maintenance system designed to predict equipment failure using real-time sensor data. The project focuses on minimizing unscheduled downtime in industrial environments by enabling data-driven maintenance decisions.

---

## 📌 Problem Statement
Traditional maintenance strategies such as reactive and time-based preventive maintenance often lead to unexpected equipment failures, high repair costs, and production losses. In heavy industries, even a single missed failure can cause significant operational disruption.

---

## 💡 Solution Overview
This project implements a **Predictive Maintenance (PdM)** approach using machine learning to:
- Monitor equipment health in real time
- Predict the probability of failure before breakdown
- Generate early alerts for maintenance teams
- Reduce operational risk and downtime

---

## 🧠 Machine Learning Approach
- **Problem Type:** Binary Classification (Failure / No Failure)
- **Baseline Model:** Logistic Regression
- **Final Model:** Random Forest Classifier

### Model Performance
- **Accuracy:** 0.94  
- **Recall:** 0.88  
- **Precision:** 0.81  

The model prioritizes **Recall** to minimize missed failures, as the cost of failure is significantly higher than the cost of preventive inspection.

---

## ⚠️ Alert Threshold Logic
- An alert is triggered when **Predicted Failure Probability ≥ 0.65**
- This threshold is intentionally chosen to reduce false negatives
- Aligns machine learning output with real-world business risk

---

## 🏗️ System Architecture
The system follows a modular architecture:
1. **Data Source Layer** – Simulated real-time sensor data (usage hours, temperature, vibration, pressure)
2. **Application Layer** – Flask backend hosting the ML model and APIs
3. **Data Layer** – SQLite database for history and audit trail
4. **Presentation Layer** – Web dashboard built using HTML templates

---

## 🛠️ Technology Stack
- **Programming Language:** Python  
- **Machine Learning:** Scikit-learn  
- **Backend:** Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS  
- **Environment:** Python Virtual Environment (venv)

---

## 📊 Key Features
- Real-time sensor data simulation
- Failure probability prediction
- Threshold-based alerting system
- Secure and structured backend
- Scalable and Industry 4.0–ready design

---

## 🚀 Future Enhancements
- Integration with real PLC / SCADA systems
- Advanced time-series models (LSTM, RUL prediction)
- Cloud deployment for scalability
- Multi-machine monitoring support

---

## 👨‍🎓 Project Details
- **Project Type:** Industry-Oriented Machine Learning Project  
- **Domain:** Predictive Analytics, Industry 4.0  
- **Developer:** Krs Ranjan  
- **Use Case:** Industrial Equipment Maintenance  

---

## 📜 License
This project is developed for academic and educational purposes.
