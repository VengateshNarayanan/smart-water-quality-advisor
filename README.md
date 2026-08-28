# 💧 Smart Water Quality Advisor

### AI-Powered Water Quality Monitoring, Forecasting & Advisory System

An intelligent web-based water quality advisory system that combines **machine-learning forecasting**, **deterministic safety rules**, and **Google Gemini AI** to analyze turbidity data and provide clear, responsible water-quality insights.

---

## 🌐 Live Demo

### 🚀 Deployed Application

> **Render Deployment:**
> https://smart-water-quality-advisor-5.onrender.com

**Example:**

```text
https://your-project-name.onrender.com
```

> Replace the placeholder above with your actual Render URL.

---

## 📌 Project Overview

The **Smart Water Quality Advisor** is designed to transform water-quality sensor data into understandable and actionable information.

The system analyzes historical river water-quality data, uses a trained machine-learning model to forecast turbidity, evaluates the predicted condition using deterministic safety rules, and provides an AI-generated advisory through a chatbot.

The application is designed to clearly distinguish between:

* **Measured water-quality values**
* **Machine-learning predictions**
* **Rule-based safety assessment**
* **AI-generated explanations**

This separation helps maintain transparency and prevents the AI layer from independently inventing environmental measurements or safety thresholds.

---

## 🎯 Objectives

* Monitor water-quality conditions using sensor data.
* Forecast turbidity using machine learning.
* Determine risk levels using deterministic rules.
* Generate understandable water-quality advisories.
* Provide an interactive AI chatbot for user questions.
* Clearly distinguish measured values from predicted values.
* Provide a responsible advisory rather than a regulatory determination.
* Deploy the complete application as a web service.

---

## ✨ Key Features

### 📊 Real-Time-Style Water Quality Dashboard

Displays:

* Current turbidity
* Predicted turbidity
* Observation timestamp
* Calculated risk level
* Safety assessment
* AI-generated recommendation

---

### 🤖 AI Water Advisor

Users can ask questions such as:

```text
What is the current turbidity?

What is the predicted turbidity?

What is the current risk level?

Why is the water classified as high risk?

What monitoring action do you recommend?

Is the turbidity expected to increase or decrease?
```

The chatbot receives verified information from the application's assessment pipeline before generating its response.

---

### 🧠 Machine-Learning Forecasting

The system uses a trained machine-learning model to forecast turbidity based on engineered water-quality features.

The trained model is stored in compressed format:

```text
turbidity_model.pkl.gz
```

This reduces the model size significantly and makes repository-based deployment more practical.

---

### 🛡️ Deterministic Safety Assessment

The safety layer evaluates the predicted turbidity using predefined application rules.

The AI model **does not determine the risk level**.

Instead:

```text
Sensor Data
     ↓
Machine Learning Prediction
     ↓
Deterministic Safety Rules
     ↓
Risk Level
     ↓
Gemini AI Explanation
```

This architecture improves consistency and transparency.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   River Sensor Data  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Cleaning &       │
                    │ Feature Engineering  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Machine Learning     │
                    │ Turbidity Model      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Predicted Turbidity  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Deterministic Safety │
                    │ Assessment           │
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
             ┌──────────────┐    ┌──────────────┐
             │ Risk Level   │    │ Safety       │
             │              │    │ Advisory     │
             └──────┬───────┘    └──────┬───────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌──────────────────────┐
                    │ Google Gemini AI     │
                    │ Advisory / Chatbot   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Flask Web Application │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      User Interface  │
                    └──────────────────────┘
```

---

## 🧰 Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API

### Backend

* Python
* Flask
* Gunicorn

### Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Joblib

### AI

* Google Gemini API
* `google-genai`

### Data Processing

* Pandas
* NumPy
* Feature Engineering
* Data Cleaning

### Deployment

* GitHub
* Render
* Gunicorn

---

## 📂 Project Structure

```text
smart-water-quality-advisor/
│
├── app.py
├── DECISION.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── river.csv
│   ├── river_cleaned.csv
│   └── river_features.csv
│
├── models/
│   └── turbidity_model.pkl.gz
│
├── src/
│   ├── advisor.py
│   ├── clean_data.py
│   ├── feature_engineering.py
│   ├── inspect_data.py
│   ├── llm_recommendation.py
│   ├── predict.py
│   ├── safety.py
│   └── train_model.py
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    └── index.html
```

---

## 🔄 Application Workflow

### 1. Data Processing

Historical water-quality data is cleaned and transformed into model-ready features.

### 2. Feature Engineering

Relevant features are generated from the processed river dataset.

### 3. Machine-Learning Prediction

The trained model predicts future turbidity.

### 4. Safety Assessment

The predicted turbidity is evaluated using deterministic application rules.

### 5. AI Advisory

Verified assessment information is provided to Google Gemini to generate a concise explanation and recommendation.

### 6. User Interaction

The Flask backend exposes the assessment and chatbot APIs to the web interface.

---

## 🔌 API Endpoints

### `GET /`

Loads the main Smart Water Quality Advisor dashboard.

---

### `GET /api/advisory`

Returns the latest water-quality assessment.

Example response:

```json
{
  "success": true,
  "data": {
    "assessment": {
      "timestamp": "2020-04-01 23:00:00",
      "current_turbidity": 11.44,
      "predicted_turbidity": 10.2106,
      "unit": "NTU",
      "risk_level": "High",
      "safety_advisory": "Turbidity is high. Closer monitoring is recommended."
    },
    "recommendation": "AI-generated advisory"
  }
}
```

---

### `POST /api/chat`

Accepts a user question and returns an AI-generated response based on the verified water-quality assessment.

Request:

```json
{
  "message": "What is the current turbidity?"
}
```

---

### `GET /health`

Health-check endpoint.

Example:

```json
{
  "status": "healthy",
  "application": "Smart Water Quality Advisory Assistant"
}
```

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/VengateshNarayanan/smart-water-quality-advisor.git
```

### 2. Enter the project directory

```bash
cd smart-water-quality-advisor
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 4. Activate the environment

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔐 Gemini API Configuration

The application requires a Gemini API key for AI-generated recommendations and chatbot responses.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

Verify:

```powershell
python -c "import os; print('SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

### Important

Never commit your API key to GitHub.

The API key should be stored as an environment variable.

For Render deployment, configure:

```text
GEMINI_API_KEY = YOUR_GEMINI_API_KEY
```

under the service's environment variables.

---

## ▶️ Run Locally

Start the Flask application:

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🚀 Deployment

The application is configured for deployment using **Render**.

### Build Command

```text
pip install -r requirements.txt
```

### Start Command

```text
gunicorn app:app
```

### Required Environment Variable

```text
GEMINI_API_KEY
```

The trained model is stored as:

```text
models/turbidity_model.pkl.gz
```

to keep the repository deployment-friendly.

---

## 📈 Machine Learning Pipeline

The project follows the following ML workflow:

```text
Raw Dataset
     ↓
Data Inspection
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Model Training
     ↓
Model Evaluation
     ↓
Model Serialization
     ↓
Compressed Model
     ↓
Prediction
```

The trained model package contains:

```python
{
    "model": trained_model,
    "features": [...],
    "target": "..."
}
```

This allows the prediction pipeline to automatically use the same feature set used during training.

---

## 🛡️ Safety & Responsible AI

This project intentionally separates **deterministic assessment** from **generative AI**.

The Gemini chatbot is instructed to:

* Use only verified application data.
* Never invent sensor measurements.
* Never invent environmental thresholds.
* Never modify the calculated risk level.
* Distinguish measured values from predictions.
* Avoid claiming that river water is safe for drinking.
* Avoid medical advice.
* State when available information is insufficient.

The AI component is therefore used primarily for **explanation and advisory communication**, rather than being the authority responsible for calculating the underlying risk.

---

## ⚠️ Limitations

This system is an educational and technical demonstration.

It should **not** be treated as:

* A certified water-quality monitoring system.
* A replacement for laboratory testing.
* A regulatory compliance system.
* A public-health decision-making system.
* A guarantee that water is safe for consumption.

The predictions depend on the quality and characteristics of the available dataset.

---

## 📊 Dataset

The project uses historical river water-quality data containing sensor observations used for data processing, feature engineering, and turbidity forecasting.

The model's predictions are dependent on the characteristics and limitations of the underlying dataset.

---

## 🔮 Future Improvements

Potential future development includes:

* Additional water-quality parameters such as pH, temperature, conductivity, and nitrate.
* Real-time IoT sensor integration.
* Time-series forecasting models.
* Automated anomaly detection.
* Historical trend visualization.
* Geographic water-quality mapping.
* Database-backed sensor storage.
* Authentication and role-based dashboards.
* Model monitoring and automated retraining.
* More comprehensive environmental risk assessment.

---

## 🎓 Project Purpose

This project was developed as a practical implementation of:

* Machine Learning
* Data Processing
* Feature Engineering
* Python Backend Development
* REST APIs
* Generative AI
* Frontend Development
* Model Deployment
* Responsible AI Design

It demonstrates how machine-learning predictions and generative AI can be combined into a practical decision-support application while maintaining a clear distinction between **verified numerical analysis** and **AI-generated explanations**.

---

## 👨‍💻 Author

### Vengatesh Narayanan

B.Tech Computer Science Engineering

Interested in:

* Machine Learning
* Artificial Intelligence
* Python
* Web Development
* Data Science
* IoT
* Cybersecurity

---

## ⭐ Acknowledgements

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy
* Google Gemini
* Render
* GitHub

---

## 📜 Disclaimer

> This system provides an advisory based on sensor data and machine-learning forecasts. It is not a regulatory determination and should not be used as a substitute for certified water-quality testing or official environmental guidance.

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

```
```
