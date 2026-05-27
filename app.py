import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from src.black_scholes import BlackScholesPricer
from src.simulation import MonteCarloPricer
from src.heston import HestonMonteCarlo
from src.vectorized_engine import VectorizedPricer

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Quant Options Engine", layout="wide", page_icon="📈")
st.title("📈 Quantitative Options Pricing Engine")
st.markdown("แพลตฟอร์มวิเคราะห์และประเมินราคาตราสารอนุพันธ์ (Institutional-Grade)")

# แถบเครื่องมือด้านข้าง
st.sidebar.header("⚙️ กำหนดพารามิเตอร์พื้นฐาน")
S = st.sidebar.number_input("ราคาหุ้นปัจจุบัน (Spot Price)", value=100.0, step=1.0)
K = st.sidebar.number_input("ราคาใช้สิทธิ (Strike Price)", value=100.0, step=1.0)
T = st.sidebar.slider("ระยะเวลาจนหมดอายุ (ปี)", min_value=0.1, max_value=5.0, value=1.0)
r = st.sidebar.slider("อัตราดอกเบี้ย (Risk-free Rate)", min_value=0.0, max_value=0.2, value=0.05)
sigma = st.sidebar.slider("ความผันผวน (Volatility)", min_value=0.01, max_value=1.0, value=0.20)

# สร้างแท็บสำหรับแสดงผล 4 โมเดล
tab1, tab2, tab3, tab4 = st.tabs(["📊 Black-Scholes", "🎲 Monte Carlo", "🌪️ Heston Model", "🚀 Batch Processing (Portfolio)"])

with tab1:
    st.subheader("Black-Scholes Analytical Pricing & Greeks")
    bs = BlackScholesPricer(S, K, T, r, sigma)
    call_metrics = bs.get_all_metrics('call')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Call Price", f"${call_metrics['Price']:.4f}")
    col2.metric("Delta (Δ)", f"{call_metrics['Delta']:.4f}")
    col3.metric("Gamma (Γ)", f"{call_metrics['Gamma']:.4f}")
    col4.metric("Vega (ν)", f"{call_metrics['Vega']:.4f}")
    col5.metric("Theta (Θ)", f"{call_metrics['Theta']:.4f}")

with tab2:
    st.subheader("Geometric Brownian Motion Simulation")
    num_paths = st.slider("จำนวนเส้นทางจำลอง", 100, 5000, 1000)
    if st.button("▶️ รันการจำลอง Monte Carlo"):
        with st.spinner('กำลังคำนวณ...'):
            mc = MonteCarloPricer(S, K, T, r, sigma, num_paths=num_paths, num_steps=252)
            mc.calculate_prices()
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(mc.simulated_paths[:100, :].T, lw=0.5, alpha=0.6)
            ax.axhline(K, color='red', linestyle='--', label='Strike Price')
            st.pyplot(fig)

with tab3:
    st.subheader("Heston Stochastic Volatility Model")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        kappa = st.number_input("Kappa (Mean Reversion Speed)", value=2.0)
        theta = st.number_input("Theta (Long-term Variance)", value=0.04)
    with col_h2:
        xi = st.number_input("Xi (Vol of Vol)", value=0.1)
        rho = st.slider("Rho (Correlation)", -1.0, 1.0, -0.7)
        
    if st.button("▶️ รันการจำลอง Heston"):
        with st.spinner('กำลังแก้สมการ SDE...'):
            heston = HestonMonteCarlo(S, sigma**2, kappa, theta, xi, rho, r, T, num_paths=1000)
            st.success(f"**ราคา Call Option (Heston): ${heston.calculate_option_price(K, 'call'):.4f}**")

with tab4:
    st.subheader("🌐 Multi-Asset Portfolio Risk Dashboard (Live Data)")
    st.markdown("วิเคราะห์และประเมินความเสี่ยง Options ของหุ้นหลายตัวพร้อมกัน (Aggregated Risk)")
    
    # ให้ผู้ใช้พิมพ์ชื่อหุ้นที่ต้องการ (คั่นด้วยลูกน้ำ)
    tickers_input = st.text_input("ระบุชื่อหุ้นในพอร์ต (เช่น AAPL, MSFT, TSLA, NVDA):", "AAPL, MSFT, NVDA")
    
    if st.button("⚡ ดึงข้อมูลจริงและวิเคราะห์ทั้งพอร์ตโฟลิโอ"):
        tickers_list = [t.strip().upper() for t in tickers_input.split(',')]
        
        with st.spinner(f'กำลังดึงข้อมูล Options ของ {", ".join(tickers_list)} จากตลาด และคำนวณผ่าน Vectorized Engine...'):
            from src.market_data import MarketDataFeed
            
            # 1. ดึงข้อมูลจริงทั้งหมดมามัดรวมกัน
            portfolio_df = MarketDataFeed.get_portfolio_options(tickers_list)
            
            if portfolio_df is not None and not portfolio_df.empty:
                r = 0.05 # Risk-free rate
                
                start_time = time.time()
                
                # 2. คำนวณราคาทฤษฎี (Theoretical Price) ของทุกตัวพร้อมกัน
                portfolio_df['Theoretical_Price'] = VectorizedPricer.black_scholes_batch(
                    S=portfolio_df['Spot'].values, 
                    K=portfolio_df['strike'].values, 
                    T=portfolio_df['T'].values, 
                    r=r, 
                    sigma=portfolio_df['impliedVolatility'].values, 
                    option_type='call'
                )
                
                # 3. คำนวณ Greeks (ความเสี่ยง) ของทุกตัวพร้อมกัน
                greeks = VectorizedPricer.greeks_batch(
                    S=portfolio_df['Spot'].values, 
                    K=portfolio_df['strike'].values, 
                    T=portfolio_df['T'].values, 
                    r=r, 
                    sigma=portfolio_df['impliedVolatility'].values, 
                    option_type='call'
                )
                
                # นำค่า Greeks ไปใส่ใน DataFrame
                portfolio_df['Delta'] = greeks['Delta']
                portfolio_df['Gamma'] = greeks['Gamma']
                portfolio_df['Vega'] = greeks['Vega']
                
                calc_time = time.time() - start_time
                
                st.success(f"✅ วิเคราะห์ Options ทั้งตลาดจำนวน **{len(portfolio_df):,} สัญญา** เสร็จสิ้นในเวลา **{calc_time:.4f} วินาที!**")
                
                # 4. แสดงผลแบบ Aggregated Risk (ความเสี่ยงรวมรายสินทรัพย์)
                st.markdown("### 📊 สรุปความเสี่ยงรวมจำแนกตามสินทรัพย์ (Risk Exposure by Asset)")
                
                # จัดกลุ่มข้อมูล (Group By) ตาม Ticker แล้วหาผลรวมความเสี่ยง
                risk_summary = portfolio_df.groupby('Ticker')[['Delta', 'Gamma', 'Vega']].sum().reset_index()
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(risk_summary.style.format({'Delta': '{:.2f}', 'Gamma': '{:.2f}', 'Vega': '{:.2f}'}))
                with col2:
                    # พล็อตกราฟเปรียบเทียบค่า Vega (ความเสี่ยงจากความผันผวน) ของแต่ละหุ้น
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.bar(risk_summary['Ticker'], risk_summary['Vega'], color='orange', alpha=0.8)
                    ax.set_title("Total Vega Exposure by Asset")
                    ax.set_ylabel("Total Vega")
                    ax.grid(axis='y', alpha=0.3)
                    st.pyplot(fig)
                
                # 5. แสดงตารางข้อมูลดิบ (ตัดมาเฉพาะคอลัมน์สำคัญ)
                st.markdown("### 🗃️ ข้อมูลตาราง Options ทั้งพอร์ต (Raw Data)")
                display_cols = ['Ticker', 'strike', 'lastPrice', 'Theoretical_Price', 'impliedVolatility', 'Delta', 'Vega']
                st.dataframe(portfolio_df[display_cols])
                
            else:
                st.error("ไม่สามารถดึงข้อมูลได้ โปรดตรวจสอบชื่อหุ้น (Ticker) อีกครั้ง")