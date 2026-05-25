# 📈 Options Pricing & Simulation Engine

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Topic](https://img.shields.io/badge/Finance-Quantitative%20Analysis-orange)

โปรเจกต์นี้คือเครื่องมือสำหรับคำนวณราคาและประเมินความเสี่ยงของตราสารอนุพันธ์ (European Options) โดยสร้างขึ้นด้วยภาษา Python โปรเจกต์นี้ผสานรวมทฤษฎีทางคณิตศาสตร์การเงินเข้ากับการเขียนโปรแกรมเชิงวัตถุ (OOP) เพื่อให้ระบบมีความยืดหยุ่นและขยายผลต่อได้ง่าย

## ✨ ฟีเจอร์หลัก (Key Features)

* **Analytical Pricing:** คำนวณราคา Call/Put Option ตามทฤษฎีด้วยสมการ Black-Scholes-Merton
* **Risk Metrics (The Greeks):** คำนวณค่าความไวต่อความเสี่ยง ได้แก่ Delta, Gamma, Vega และ Theta
* **Numerical Simulation:** จำลองเส้นทางราคาในอนาคตด้วย Geometric Brownian Motion (GBM) ผ่านวิธี Monte Carlo Simulation
* **Data Visualization:** แสดงผลกราฟจำลองเส้นทางราคาสินทรัพย์ (Simulation Paths) และกราฟโปรไฟล์ความเสี่ยง (Greeks Profile) ได้อย่างสวยงามด้วย Matplotlib และ Seaborn

## 🧮 พื้นฐานทางคณิตศาสตร์ (Mathematical Foundation)

โปรเจกต์นี้ขับเคลื่อนด้วย 2 โมเดลหลัก:

**1. Black-Scholes Model**
สมการปิดสำหรับหาราคาทางทฤษฎีของ Call Option:
$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

**2. Geometric Brownian Motion (GBM)**
สมการเชิงอนุพันธ์สุ่ม (SDE) สำหรับจำลองการเคลื่อนที่ของราคาสินทรัพย์:
$$dS_t = r S_t dt + \sigma S_t dW_t$$

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
options_pricing_engine/
│
├── src/                        # Core Engine Modules
│   ├── __init__.py
│   ├── black_scholes.py        # BSM Analytical Pricer & Greeks
│   ├── simulation.py           # Monte Carlo & GBM Simulator
│   └── visualization.py        # Chart Plotting & Visuals
│
├── notebooks/                  # Jupyter Notebooks for Presentation
│   └── portfolio_demo.ipynb    # สรุปผลการทดลองและการทำงาน
│
├── main.py                     # Main script สำหรับทดสอบการรันโปรเจกต์
├── requirements.txt            # รายชื่อไลบรารีที่จำเป็นต้องใช้
└── README.md                   # ไฟล์เอกสารของโปรเจกต์นี้