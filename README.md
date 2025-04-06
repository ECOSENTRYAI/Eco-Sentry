#  EcoSentry – AI-Powered Wildfire Prediction System

EcoSentry is a real-time wildfire risk prediction and alerting platform powered by satellite data, AI, and geospatial analytics. Designed to help governments, emergency responders, NGOs, and citizens take preemptive action before disaster strikes.

##  Problem

Every year, wildfires cause widespread destruction—impacting lives, biodiversity, and the environment. Early detection and fast response are critical to minimizing damage. EcoSentry addresses this by combining satellite intelligence with AI to provide timely alerts and insights.

---

##  Features

-  **Real-time wildfire risk prediction**
-  **AI-powered analysis of satellite and weather data**
-  **Interactive risk maps with geospatial visualization**
-  **Instant alerts via SMS and dashboard**
-  **Multi-threat detection (fire, deforestation)**
-  **Integration with emergency response agencies and NGOs**

---

## Tech Stack

| Layer                | Technology Used                                  |
|---------------------|---------------------------------------------------|
| Frontend            | HTML, CSS, JavaScript, React (for web MVP)        |
| Backend/API         | Python, FastAPI                                   |
| AI/ML Engine        | TensorFlow, Scikit-learn, Pandas, NumPy           |
| Satellite Data      | **Google Earth Engine**, FIRMS, MODIS, Sentinel2  |
| Cloud Services      | **Google Cloud Platform (GCP)**, **Firebase**     |
| Automation          | **Google Cloud Functions**                        |
| AI Assistant        | **Gemini API** (for user interaction, insights)   |
| DevOps              | Git, GitHub, Docker (optional)                    |

---

##  Powered by Google Technologies

- **Google Earth Engine** – To access, process, and analyze multi-temporal satellite data.
- **Firebase** – Real-time database, user alert history, and authentication.
- **Google Cloud Functions** – To handle alert triggers and scheduled processing.
- **Google Cloud Storage** – For satellite data snapshots and logs.
- **Gemini API** – Enables natural language interaction, risk query resolution, and explanations.
- **Google Cloud Platform (GCP)** – Infrastructure backbone for compute, AI model deployment, and database hosting.

---


Watch the [Demo Video ▶️](link-to-demo) to see EcoSentry in action.

---

##  Setup Instructions

```bash
git clone https://github.com/your-username/ecosentry.git
cd ecosentry
pip install -r requirements.txt
uvicorn main:app --reload
