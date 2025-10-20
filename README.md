# 🍏 Fruit & Veg Quality — Edge AI for Freshness Detection

**Fruit & Veg Quality** is an edge-AI application that uses computer vision to assess the freshness and ripeness of fruits and vegetables in real time — directly on low-power devices such as the **Raspberry Pi Zero 2W**.

The project combines **TensorFlow Lite** and **OpenCV** to enable efficient, on-device quality control — without cloud dependency or expensive hardware.

---

## 🚀 Key Features
- 🍎 **Real-time quality assessment** (unripe / fresh / rotten)  
- ⚡ **Optimized for edge devices** (Raspberry Pi Zero 2W, Jetson Nano, etc.)  
- 🧠 **Compact CNN model** based on MobileNetV2, quantized with TensorFlow Lite  
- 🎥 **Camera-based detection** using OpenCV  
- 🧰 **Fully offline**, no need for cloud connectivity  
- 🛠️ **Extensible pipeline** — retrain or replace the model via Edge Impulse  

---

## 🧠 How It Works

Camera Input → Preprocessing → TFLite Model → Quality Prediction → Display

1. Captures a live image from a connected camera  
2. Preprocesses and normalizes the frame (PIL / OpenCV)  
3. Runs inference using a quantized TensorFlow Lite model  
4. Displays prediction results (class + confidence)   

---

## 🏗️ Project Structure

---

## 🧰 Requirements

- Python 3.9+
- Raspberry Pi Zero 2W (or any Linux ARM board)
- TensorFlow Lite runtime
- Camera module (Raspberry Pi v2 or USB camera)

---

## 🧩 Installation

### 1. Clone the repository
```bash
git clone https://github.com/12FlyBreads/fruit-quality-assessment.git
cd fruit-veg-quality
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the application
```bash
```

---

## 🧑‍💻 Contributors
pithon3
```

---
