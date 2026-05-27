import pandas as pd
from src.market_data import MarketDataFeed
from src.stress_test import PortfolioStressTester

def test_portfolio_stress():
    print("=== 🚨 Portfolio Stress Testing (Scenario Analysis) ===")
    
    # 1. สร้างพอร์ตจำลองโดยดึงข้อมูลจริงของบิ๊กเทค 3 ทหารเสือ
    tickers = ["AAPL", "MSFT", "NVDA"]
    print(f"กำลังดึงข้อมูล Options ของ {tickers} จากตลาดจริง...")
    
    portfolio_df = MarketDataFeed.get_portfolio_options(tickers)
    
    if portfolio_df is None or portfolio_df.empty:
        print("ไม่สามารถสร้างพอร์ตโฟลิโอได้")
        return
        
    # สุ่มเลือกมาแค่หุ้นละ 5 สัญญาเพื่อไม่ให้ผลลัพธ์ยาวเกินไป
    portfolio_df = portfolio_df.groupby('Ticker').head(5).reset_index(drop=True)
    
    # 2. เอาพอร์ตเข้าเครื่องจำลองวิกฤต
    tester = PortfolioStressTester(portfolio_df)
    
    # 3. สถานการณ์ที่ 1: ตลาดพังพินาศ (Market Crash)
    # หุ้นตก 20% (-0.20) แต่ความผันผวนพุ่งทะลุเพดาน 50% (+0.50)
    crash_result = tester.apply_scenario(spot_shock_pct=-0.20, vol_shock_pct=0.50, scenario_name="Market Crash (-20% Spot, +50% Vol)")
    
    print("\n💥 สถานการณ์: ตลาดหุ้นร่วงหนัก 20% และความผันผวนพุ่ง 50%")
    print(crash_result[['Ticker', 'strike', 'Base_Price', 'Shocked_Price', 'PnL ($)']].to_string())
    
    total_loss = crash_result['PnL ($)'].sum()
    print(f"\n📉 มูลค่าพอร์ตโฟลิโอเปลี่ยนแปลงรวม (Total PnL): ${total_loss:,.2f}")
    
    # 4. สถานการณ์ที่ 2: สร้าง Risk Matrix เพื่อทำ Heatmap
    print("\n📊 กำลังสร้าง Risk Matrix (Spot vs Volatility)...")
    spot_shocks = [-0.20, -0.10, 0.0, 0.10, 0.20]  # หุ้นตก 20% ไปจนถึงขึ้น 20%
    vol_shocks = [0.0, 0.20, 0.50]                 # ความผันผวนคงที่ ไปจนถึงพุ่ง 50%
    
    matrix_df = tester.generate_risk_matrix(spot_shocks, vol_shocks)
    
    # จัดรูปทรงตาราง (Pivot Table) ให้ดูง่าย
    pivot_matrix = matrix_df.pivot(index='Spot_Shock', columns='Vol_Shock', values='Total_Portfolio_PnL')
    pivot_matrix.index = [f"{x*100:+.0f}%" for x in pivot_matrix.index]
    pivot_matrix.columns = [f"{x*100:+.0f}%" for x in pivot_matrix.columns]
    
    print("\n🔥 ตารางความเสี่ยง (PnL Matrix: แนวนอน=Vol Shock, แนวตั้ง=Spot Shock):")
    print(pivot_matrix.to_string())

if __name__ == "__main__":
    test_portfolio_stress()