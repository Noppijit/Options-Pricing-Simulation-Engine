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

⚙️ การติดตั้งและใช้งาน (Installation & Usage)
โคลนโปรเจกต์นี้ลงเครื่อง (Clone the repository)
git clone [https://github.com/YOUR_USERNAME/options_pricing_engine.git](https://github.com/YOUR_USERNAME/options_pricing_engine.git)
cd options_pricing_engine

ติดตั้งไลบรารีที่จำเป็น (Install dependencies)
แนะนำให้สร้าง Virtual Environment ก่อน แล้วจึงติดตั้งผ่าน requirements.txt
pip install -r requirements.txt

รันทดสอบระบบ (Run the engine)
python main.py

หมายเหตุ: เมื่อโปรแกรมทำงาน จะมีหน้าต่างกราฟเด้งขึ้นมา ให้ปิดหน้าต่างกราฟแรกก่อน โปรแกรมจึงจะแสดงกราฟถัดไป
เปิดดูผลสรุปแบบ Interactive
สามารถเปิดไฟล์ notebooks/portfolio_demo.ipynb ผ่าน Jupyter Notebook หรือ VS Code เพื่อดูการนำเสนอผลลัพธ์ทีละขั้นตอน

👨‍💻 ผู้พัฒนา (Author)
[Noppijit Payab] * LinkedIn: [www.linkedin.com/in/noppijit-payab-482535348]
Email: [noppijit.p@gmail.com]
โปรเจกต์นี้สร้างขึ้นเพื่อเป็น Portfolio สำหรับแสดงทักษะด้าน Quantitative Analysis, Data Science และ Python Programming