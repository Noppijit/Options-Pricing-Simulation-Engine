import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from src.black_scholes import BlackScholesPricer
from src.simulation import MonteCarloPricer
from src.heston import HestonMonteCarlo
from src.vectorized_engine import VectorizedPricer
from src.market_data import MarketDataFeed
from src.american_options import AmericanOptionLSM
from src.stress_test import PortfolioStressTester

# 1. ตั้งค่าหน้าเว็บและ Theme (ต้องอยู่บรรทัดแรกสุดเสมอ)
st.set_page_config(page_title="ProQuant Options Engine", layout="wide", page_icon="🏦")

# 2. สร้าง Header ที่ดูเป็นสถาบันการเงิน (Institutional Look)
st.markdown("""
<div style='text-align: center; padding: 1.5rem; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: #1e3a8a; margin-bottom: 0;'>🏦 ProQuant Options Engine</h1>
    <p style='font-size: 1.1rem; color: #4b5563; margin-top: 0.5rem;'>
        Institutional-Grade Derivatives Pricing, Simulation & Risk Management Platform
    </p>
</div>
""", unsafe_allow_html=True)

# 3. แถบ Sidebar ที่จัดหมวดหมู่พารามิเตอร์อย่างเป็นระเบียบ
with st.sidebar:
    st.header("⚙️ Global Parameters")
    st.markdown("ปรับแต่งค่าพื้นฐานสำหรับคำนวณราคาทฤษฎี")
    
    # เพิ่มคำอธิบาย (help) ให้กับทุกตัวแปร
    S = st.number_input("Spot Price ($)", value=100.0, step=1.0, help="ราคาปัจจุบันของสินทรัพย์อ้างอิงในตลาด")
    K = st.number_input("Strike Price ($)", value=100.0, step=1.0, help="ราคาใช้สิทธิที่ระบุในสัญญาออปชัน")
    T = st.slider("Time to Maturity (Years)", 0.1, 5.0, 1.0, help="ระยะเวลาคงเหลือก่อนหมดอายุ (หน่วยเป็นปี)")
    r = st.slider("Risk-Free Rate", 0.0, 0.2, 0.05, help="อัตราผลตอบแทนปราศจากความเสี่ยง (เช่น พันธบัตรรัฐบาล)")
    sigma = st.slider("Implied Volatility", 0.01, 1.0, 0.20, help="ความผันผวนแฝงที่ตลาดคาดการณ์")
    
    # ซ่อนพารามิเตอร์ขั้นสูงไว้ใน Expander เพื่อความสะอาดตา
    with st.expander("🛠️ Advanced Models Settings (Heston)"):
        st.markdown("<small>พารามิเตอร์สำหรับ Stochastic Volatility</small>", unsafe_allow_html=True)
        kappa = st.number_input("Kappa", value=2.0, help="ความเร็วในการกลับสู่ค่าเฉลี่ย (Mean Reversion Speed)")
        theta = st.number_input("Theta", value=0.04, help="ค่าเฉลี่ยความผันผวนระยะยาว (Long-term Variance)")
        xi = st.number_input("Xi (Vol of Vol)", value=0.1, help="ความผันผวนของความผันผวน")
        rho = st.slider("Rho (Correlation)", -1.0, 1.0, -0.7, help="ความสัมพันธ์ระหว่างราคาและความผันผวน (ปกติจะติดลบ)")

# 4. เปลี่ยนชื่อแท็บให้ดูโปรและจัดวางไอคอนให้สวยงาม
tabs = st.tabs([
    "1️⃣ Analytics (BSM)", 
    "2️⃣ Simulation (MC)", 
    "3️⃣ Advanced (Heston)", 
    "4️⃣ Live Portfolio", 
    "5️⃣ American Style", 
    "6️⃣ Risk (Stress Test)",
    "7️⃣ 3D Vol Surface"
])

# --- TAB 1: Analytics (BSM) ---
with tabs[0]:
    st.subheader("📊 Black-Scholes Analytics & Greeks Profile")
    bs = BlackScholesPricer(S, K, T, r, sigma)
    metrics = bs.get_all_metrics('call')
    
    st.info("💡 **Greeks** คือตัวชี้วัดความเสี่ยงที่บอกว่าราคา Option จะเปลี่ยนไปเท่าไร หากปัจจัยอื่นๆ (เช่น ราคาหุ้น, เวลา, ความผันผวน) เปลี่ยนแปลงไป 1 หน่วย")
    
    cols = st.columns(5)
    cols[0].metric("Call Price", f"${metrics['Price']:.4f}", delta="Theoretical", delta_color="off")
    cols[1].metric("Delta (Δ)", f"{metrics['Delta']:.4f}", help="ความไวต่อราคาหุ้น")
    cols[2].metric("Gamma (Γ)", f"{metrics['Gamma']:.4f}", help="ความไวของ Delta ต่อราคาหุ้น")
    cols[3].metric("Vega (ν)", f"{metrics['Vega']:.4f}", help="ความไวต่อความผันผวน")
    cols[4].metric("Theta (Θ)", f"{metrics['Theta']:.4f}", help="มูลค่าที่ลดลงตามกาลเวลา (Time Decay)")

# --- TAB 2: Simulation ---
with tabs[1]:
    st.subheader("🎲 Monte Carlo Simulation (GBM)")
    num_paths = st.slider("จำนวนเส้นทางจำลอง", 100, 5000, 1000, help="ยิ่งจำลองมาก ยิ่งแม่นยำ แต่กินทรัพยากรเครื่อง")
    if st.button("▶️ รันการจำลอง (Run Simulation)", use_container_width=True):
        with st.spinner('กำลังประมวลผลเส้นทางแบบสุ่ม...'):
            mc = MonteCarloPricer(S, K, T, r, sigma, num_paths=num_paths, num_steps=252)
            mc.calculate_prices()
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(mc.simulated_paths[:100, :].T, lw=0.5, alpha=0.6)
            ax.axhline(K, color='red', linestyle='--', label='Strike Price')
            ax.set_title("Geometric Brownian Motion (First 100 Paths)")
            ax.set_xlabel("Trading Days")
            ax.set_ylabel("Asset Price ($)")
            ax.legend()
            st.pyplot(fig)

# --- TAB 3: Advanced Models ---
with tabs[2]:
    st.subheader("🌪️ Heston Stochastic Volatility Model")
    st.markdown("การประเมินราคาโดยอ้างอิง **Stochastic Volatility** (ความผันผวนที่ไม่คงที่) ซึ่งสะท้อนความจริงของตลาดได้ดีกว่า Black-Scholes")
    if st.button("▶️ ประมวลผล Heston Model", use_container_width=True):
        with st.spinner('กำลังแก้สมการเชิงอนุพันธ์สุ่ม (SDE)...'):
            heston = HestonMonteCarlo(S, sigma**2, kappa, theta, xi, rho, r, T, num_paths=1000)
            st.success(f"**ราคา Call Option อ้างอิง Heston Model: ${heston.calculate_option_price(K, 'call'):.4f}**")

# --- TAB 4: Live Portfolio ---
with tabs[3]:
    st.subheader("🌐 Cross-Asset Portfolio Pricing (Vectorized)")
    tickers_input = st.text_input("ระบุ Ticker (คั่นด้วยลูกน้ำ):", "AAPL, MSFT, TSLA", help="ใส่ชื่อหุ้นที่จดทะเบียนในตลาดอเมริกา")
    if st.button("⚡ ดึงข้อมูลตลาดจริง (Live Market Data)", use_container_width=True):
        tickers_list = [t.strip().upper() for t in tickers_input.split(',')]
        with st.spinner('Fetching Live Data via Yahoo Finance & Processing Vectorization...'):
            portfolio_df = MarketDataFeed.get_portfolio_options(tickers_list)
            if portfolio_df is not None and not portfolio_df.empty:
                portfolio_df['Theoretical_Price'] = VectorizedPricer.black_scholes_batch(
                    S=portfolio_df['Spot'].values, K=portfolio_df['strike'].values, 
                    T=portfolio_df['T'].values, r=0.05, sigma=portfolio_df['impliedVolatility'].values, option_type='call'
                )
                st.dataframe(portfolio_df[['Ticker', 'strike', 'lastPrice', 'Theoretical_Price', 'impliedVolatility', 'Spot', 'T']].head(15), use_container_width=True)
            else:
                st.error("ดึงข้อมูลล้มเหลว โปรดตรวจสอบชื่อ Ticker")

# --- TAB 5: American Options ---
with tabs[4]:
    st.subheader("🇺🇸 American Options (Longstaff-Schwartz)")
    am_ticker = st.text_input("ระบุชื่อหุ้น 1 ตัว:", "TSLA", key="am_ticker")
    if st.button("⚡ คำนวณ Early Exercise Premium", use_container_width=True):
        with st.spinner('Running Least Squares Monte Carlo (LSM)...'):
            df_am = MarketDataFeed.get_portfolio_options([am_ticker])
            if df_am is not None and not df_am.empty:
                target_opt = df_am.iloc[len(df_am)//2] 
                bs_am = BlackScholesPricer(target_opt['Spot'], target_opt['strike'], target_opt['T'], 0.05, target_opt['impliedVolatility'])
                euro_price = bs_am.put_price()
                lsm = AmericanOptionLSM(target_opt['Spot'], target_opt['strike'], target_opt['T'], 0.05, target_opt['impliedVolatility'])
                american_price = lsm.price('put')
                
                st.markdown(f"**สินทรัพย์:** `{target_opt['Ticker']}` | **Spot:** `${target_opt['Spot']:.2f}` | **Strike:** `${target_opt['strike']:.2f}`")
                c1, c2, c3 = st.columns(3)
                c1.metric("European Put", f"${euro_price:.4f}")
                c2.metric("American Put", f"${american_price:.4f}", delta=f"+${american_price - euro_price:.4f} Premium")
                c3.metric("Live Market Price", f"${target_opt['lastPrice']:.4f}")
            else:
                st.error("ดึงข้อมูลล้มเหลว")

# --- TAB 6: Stress Testing ---
with tabs[5]:
    st.subheader("🚨 Portfolio Scenario Analysis (Stress Test)")
    if st.button("🔥 รัน PnL Shock Matrix", use_container_width=True):
        with st.spinner('Calculating Portfolio Exposures...'):
            df_port = MarketDataFeed.get_portfolio_options(["AAPL", "MSFT"])
            if df_port is not None and not df_port.empty:
                tester = PortfolioStressTester(df_port.head(100))
                spot_shocks = np.linspace(-0.30, 0.30, 7)
                vol_shocks = np.array([0.0, 0.25, 0.50, 0.75])
                matrix_df = tester.generate_risk_matrix(spot_shocks, vol_shocks)
                pivot_df = matrix_df.pivot(index='Spot_Shock', columns='Vol_Shock', values='Total_Portfolio_PnL')
                pivot_df.index = [f"{x*100:+.0f}%" for x in pivot_df.index]
                pivot_df.columns = [f"{x*100:+.0f}%" for x in pivot_df.columns]
                
                st.markdown("#### Portfolio PnL Heatmap ($)")
                st.dataframe(pivot_df.style.background_gradient(cmap='RdYlGn', axis=None).format("{:,.2f}"), use_container_width=True)
            else:
                st.error("เกิดข้อผิดพลาดในการดึงข้อมูลพอร์ต")

# --- TAB 7: 3D Vol Surface ---
with tabs[6]:
    st.subheader("🌐 Implied Volatility Surface (3D)")
    surf_ticker = st.text_input("ระบุชื่อหุ้น:", "AAPL", key="surf_ticker")
    if st.button("📈 พล็อต 3D Surface", use_container_width=True):
        with st.spinner("Fetching Options Chains across multiple expirations..."):
            surf_df = MarketDataFeed.get_volatility_surface(surf_ticker)
            if surf_df is not None and not surf_df.empty:
                fig = go.Figure(data=[go.Scatter3d(
                    x=surf_df['strike'], y=surf_df['T'], z=surf_df['impliedVolatility'],
                    mode='markers', marker=dict(size=5, color=surf_df['impliedVolatility'], colorscale='Viridis', opacity=0.8)
                )])
                fig.update_layout(
                    scene=dict(xaxis_title='Strike', yaxis_title='Time (Years)', zaxis_title='Implied Volatility'),
                    height=600, margin=dict(l=0, r=0, b=0, t=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("ไม่สามารถสร้าง 3D Surface ได้")