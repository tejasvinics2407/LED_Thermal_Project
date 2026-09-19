# AI/ML-Based LED Thermal Monitoring and Predictive Maintenance System

An AI/ML-based system for monitoring the thermal and electrical behaviour of LED luminaires, predicting junction temperature, identifying critical thermal conditions, and providing predictive maintenance recommendations.

---

## 📌 Overview

LED luminaires generate heat during operation, and excessive temperature can affect their performance, reliability, and lifespan.

This project presents a software-based **LED Thermal Monitoring and Predictive Maintenance System** that uses telemetry data and Machine Learning to estimate the LED junction temperature.

The system processes parameters such as ambient temperature, heat sink temperature, current, voltage, electrical power, and dimming level. An **XGBoost regression model** is used to predict junction temperature, while a **FastAPI backend** and **Streamlit dashboard** provide an interface for monitoring and visualization.

The current implementation uses generated telemetry data and is designed to serve as a foundation for future integration with real-world LED hardware and sensors.

---

## 🎯 Objectives

- Monitor important thermal and electrical parameters of LED luminaires.
- Predict LED junction temperature using Machine Learning.
- Identify potentially critical thermal operating conditions.
- Provide maintenance recommendations based on predicted thermal conditions.
- Visualize telemetry and temperature trends through an interactive dashboard.
- Provide a foundation for future IoT and hardware-based implementation.

---

## ✨ Key Features

### 🌡️ Thermal Monitoring
- Monitoring of ambient temperature.
- Monitoring of heat sink temperature.
- Tracking of temperature trends.

### ⚡ Electrical Monitoring
- Voltage monitoring.
- Current monitoring.
- Electrical power monitoring.
- LED dimming level monitoring.

### 🤖 Machine Learning Prediction
- XGBoost regression model for predicting LED junction temperature.
- Uses multiple thermal and electrical parameters as model inputs.

### 🚨 Thermal Status Detection
- Evaluates predicted junction temperature.
- Identifies different thermal operating conditions.
- Provides a corresponding maintenance recommendation.

### 🔧 Predictive Maintenance
- Provides recommended actions when potentially critical thermal conditions are detected.
- Helps identify conditions that may require intervention.

### 🚀 FastAPI Backend
- Provides a backend API for the prediction system.
- Connects the Machine Learning model with the dashboard.

### 📊 Interactive Dashboard
- Built using Streamlit.
- Displays telemetry values, predictions, thermal status, recommendations, and temperature history.

---

## 🏗️ System Architecture

```text
                 LED Telemetry Data
                         |
                         v
                  Data Generation
                         |
                         v
                 Data Preprocessing
                         |
                         v
                  Feature Preparation
                         |
                         v
                  XGBoost ML Model
                         |
                         v
             Junction Temperature Prediction
                         |
                         v
                   FastAPI Backend
                         |
                         v
                 Streamlit Dashboard
                         |
              +----------+----------+
              |                     |
              v                     v
       Thermal Status       Maintenance
        Monitoring          Recommendation
