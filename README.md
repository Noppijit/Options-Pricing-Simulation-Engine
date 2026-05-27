# 🏦 ProQuant Options Engine
*(Institutional-Grade Derivatives Pricing, Simulation & Risk Management Platform)*

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Topic](https://img.shields.io/badge/Finance-Quantitative%20Analysis-orange)
![Framework](https://img.shields.io/badge/UI-Streamlit-red)

[cite_start]โปรเจกต์นี้คือแพลตฟอร์มวิเคราะห์และประเมินราคาตราสารอนุพันธ์ระดับสถาบัน (Institutional-Grade) ที่พัฒนาด้วย Python และแสดงผลผ่าน Streamlit Web Dashboard รองรับการดึงข้อมูลจริงจากตลาด (Live Data) และใช้โมเดลคณิตศาสตร์การเงินขั้นสูง 

## ✨ ฟีเจอร์หลัก (Key Features)

* [cite_start]**Interactive Web Dashboard:** หน้าจอผู้ใช้งานแบบ UI/UX ระดับมืออาชีพ (สร้างด้วย Streamlit) 
* [cite_start]**Live Market Data:** เชื่อมต่อ API ของ Yahoo Finance เพื่อดึงข้อมูล Options ของหุ้นสหรัฐฯ แบบเรียลไทม์ 
* [cite_start]**Advanced Options Pricing:** * *European Options:* คำนวณด้วย Black-Scholes-Merton (BSM) พร้อมแสดงผล Risk Metrics (The Greeks) ครบถ้วน 
  * [cite_start]*American Options:* ใช้อัลกอริทึม Longstaff-Schwartz (Least Squares Monte Carlo) เพื่อประเมินมูลค่า Early Exercise Premium 
* [cite_start]**Stochastic Volatility:** จำลองความผันผวนที่ไม่คงที่ตามสภาพตลาดจริงด้วย Heston Model 
* [cite_start]**High-Performance Computing:** ประมวลผลพอร์ตโฟลิโอหลายสินทรัพย์ (Multi-Asset) พร้อมกันในเสี้ยววินาทีด้วยเทคนิค Vectorization ผ่าน NumPy 
* [cite_start]**Risk Management & Stress Testing:** สร้าง Scenario Analysis เพื่อดูผลกระทบต่อพอร์ตโฟลิโอในสภาวะวิกฤต พร้อมแสดงผลรูปแบบ PnL Heatmap 
* [cite_start]**3D Volatility Surface:** กวาดข้อมูลและพล็อตกราฟ 3 มิติ เพื่อวิเคราะห์โครงสร้างความผันผวน (Term Structure & Volatility Smile) 

## 🧮 พื้นฐานทางคณิตศาสตร์ (Mathematical Foundation)

[cite_start]โปรเจกต์นี้ขับเคลื่อนด้วยโมเดลคณิตศาสตร์การเงินระดับสูง ได้แก่: 
1. [cite_start]**Black-Scholes-Merton (BSM):** สมการปิดสำหรับหา Theoretical Price ของ European Option 
2. [cite_start]**Geometric Brownian Motion (GBM):** สมการเชิงอนุพันธ์สุ่ม (SDE) เพื่อจำลองเส้นทางราคาผ่าน Monte Carlo 
3. [cite_start]**Heston Stochastic Volatility Model:** ระบบสมการ SDE คู่ขนานเพื่อจำลองการแกว่งตัวของความผันผวน (Mean Reversion) 
4. [cite_start]**Least Squares Monte Carlo (LSM):** การทำ Polynomial Regression ย้อนกลับเพื่อตัดสินใจจุดใช้สิทธิก่อนกำหนด 

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
options_pricing_engine/
│
├── src/                        # Core Engine Modules
│   ├── __init__.py
│   ├── black_scholes.py        # BSM Analytical Pricer & Greeks
│   ├── simulation.py           # Monte Carlo & GBM Simulator
│   ├── visualization.py        # Chart Plotting & Visuals
│   ├── heston.py               # Heston Stochastic Volatility Model
│   ├── market_data.py          # Yahoo Finance API & Live Data integration
│   ├── vectorized_engine.py    # High-Performance Portfolio Pricer
│   ├── american_options.py     # Longstaff-Schwartz Method
│   └── stress_test.py          # Portfolio Scenario Analysis
│
├── app.py                      # 🌟 Streamlit Web Dashboard (Main UI)
├── main.py                     # Script สำหรับรันทดสอบอัลกอริทึมหลังบ้าน
├── requirements.txt            # รายชื่อไลบรารีที่จำเป็นสำหรับการ Deploy
└── README.md                   # ไฟล์เอกสารของโปรเจกต์นี้

⚙️ การติดตั้งและใช้งาน (Installation & Usage)
1. โคลนโปรเจกต์นี้ลงเครื่อง (Clone the repository)
git clone [https://github.com/Noppijit/Options-Pricing-Simulation-Engine](https://github.com/Noppijit/Options-Pricing-Simulation-Engine.git)
cd options_pricing_engine

2. ติดตั้งไลบรารีที่จำเป็น (Install dependencies)
pip install -r requirements.txt

3. เปิดใช้งาน Web Dashboard (Launch the Platform)
streamlit run app.py

4. ทดสอบความถูกต้องของโมเดลทางคณิตศาสตร์
python main.py

👨‍💻 ผู้พัฒนา (Author)
Noppijit Payab
LinkedIn: www.linkedin.com/in/noppijit-payab-482535348
Email: noppijit.p@gmail.com

โปรเจกต์นี้สร้างขึ้นเพื่อเป็น Portfolio สำหรับแสดงทักษะระดับสูงด้าน Quantitative Analysis, Financial Engineering, Risk Management และ Python Programming