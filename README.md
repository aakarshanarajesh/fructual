# 🍓 FRUCTUAL – AI-Based Smart Sugar Recommendation & Dispensing System

## 🔍 Overview

FRUCTUAL is an AI-driven personalized sugar recommendation and dispensing system designed for diabetic and fitness users. It analyzes user health data and intelligently determines the safest and most suitable sugar intake using natural fruit-based alternatives.

---

## 🎯 Problem Statement

Managing sugar intake is critical for diabetic patients and health-conscious individuals. Existing systems either:

* Only monitor glucose
* Only provide suggestions
* Or lack real-time personalized control

There is no integrated system that combines **health analysis + decision-making + automated dispensing**.

---

## 💡 Solution

FRUCTUAL provides a complete solution by:

* Analyzing user health parameters (age, BMI, blood sugar, activity)
* Applying adaptive AI logic
* Recommending precise sugar dosage (in grams)
* Selecting optimal fruit-based sugar blends
* Controlling a real-time dispensing system using Arduino

---

## 🧠 AI Logic (Core Engine)

The system calculates sugar dosage using:

* Blood sugar level
* BMI
* Activity level
* Diabetic condition
* Historical data (adaptive learning)

Example:

* High glucose → restrict sugar
* Low glucose → increase intake
* Previous trends → adjust recommendations

👉 Implemented in: `ai_engine.py`

---

## ⚙️ System Architecture

1. User inputs data (UI)
2. Flask backend processes request
3. AI engine computes recommendation
4. Data stored in SQLite database
5. Output displayed to user
6. Optional: Command sent to Arduino for dispensing

---

## 🚀 Features

* 🧠 AI-based sugar recommendation
* 📊 Adaptive intelligence using past data
* 🍎 Smart fruit-based sugar selection
* ⚠️ Safety control for diabetic users
* 💾 Database logging (SQLite)
* 🌐 Web interface using Flask
* ⚡ Real-time dispensing using Arduino

---

## 🛠️ Tech Stack

* Python
* Flask
* SQLite
* Machine Learning Logic (Rule-based AI)
* PySerial (Arduino communication)
* HTML, CSS

---

## ▶️ How to Run

```bash
pip install flask pyserial
python app.py
```

Open browser:

```
http://localhost:5000
```

---

## 📂 Project Structure

```
fructual/
│── app.py                # Flask backend
│── ai_engine.py          # AI decision logic
│── database.py           # Database setup
│── fructual.db           # SQLite database
│── templates/
│── static/
```

---

## 📸 Output

* Displays:

  * Recommended sugar (grams)
  * Fruit blend type
  * Health status message
  * Confidence level
  * Adaptive insights

---

## 🔌 Hardware Integration

* Arduino Uno
* Servo motor (for sugar selection)
* Load cell (weight measurement)
* Dispensing mechanism

The system sends commands via serial communication to dispense exact sugar quantity.

---

## 📈 Innovation Highlights

* Combines **AI + IoT + Healthcare**
* Uses **adaptive learning (previous data trends)**
* Integrates **decision + action (dispensing)**
* Promotes **natural sugar alternatives instead of refined sugar**

👉 As explained in project documentation , this system uniquely integrates monitoring, prediction, and automated dispensing into one platform.

---

## 🔮 Future Improvements

* IoT cloud integration
* Mobile app
* Real-time CGM sensor integration
* Deep learning model for prediction

---

## 👨‍💻 Author

Aakarshana R
