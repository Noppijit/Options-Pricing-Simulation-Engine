import numpy as np
import pandas as pd
from src.vectorized_engine import VectorizedPricer

class PortfolioStressTester:
    """
    ระบบจำลองสถานการณ์และทดสอบสภาวะวิกฤต (Stress Testing) ของพอร์ตโฟลิโอ
    """
    def __init__(self, portfolio_df, risk_free_rate=0.05):
        # รับข้อมูลพอร์ตโฟลิโอที่มีคอลัมน์ Spot, strike, T, impliedVolatility
        self.portfolio = portfolio_df.copy()
        self.r = risk_free_rate
        
        # คำนวณราคาตั้งต้น (Base Price) ก่อนโดน Shock
        self.portfolio['Base_Price'] = VectorizedPricer.black_scholes_batch(
            S=self.portfolio['Spot'].values,
            K=self.portfolio['strike'].values,
            T=self.portfolio['T'].values,
            r=self.r,
            sigma=self.portfolio['impliedVolatility'].values,
            option_type='call' # สมมติว่าเป็น Call Option ทั้งพอร์ตเพื่อความเรียบง่าย
        )

    def apply_scenario(self, spot_shock_pct, vol_shock_pct, scenario_name="Custom Shock"):
        """
        จำลองผลกระทบเมื่อราคาหุ้นและความผันผวนเปลี่ยนไป
        """
        # 1. ช็อคตัวแปร (Apply Shocks)
        shocked_spot = self.portfolio['Spot'] * (1 + spot_shock_pct)
        shocked_vol = self.portfolio['impliedVolatility'] * (1 + vol_shock_pct)
        
        # ป้องกันไม่ให้ Volatility ติดลบ
        shocked_vol = np.maximum(shocked_vol, 0.01)
        
        # 2. คำนวณราคาใหม่ (Shocked Price)
        shocked_prices = VectorizedPricer.black_scholes_batch(
            S=shocked_spot.values,
            K=self.portfolio['strike'].values,
            T=self.portfolio['T'].values,
            r=self.r,
            sigma=shocked_vol.values,
            option_type='call'
        )
        
        # 3. คำนวณ PnL (สมมติว่า 1 สัญญา = 100 หุ้น)
        # PnL = (ราคาใหม่ - ราคาเดิม) * 100
        pnl = (shocked_prices - self.portfolio['Base_Price']) * 100
        
        # 4. สรุปผลลัพธ์
        result_df = self.portfolio[['Ticker', 'strike', 'Spot', 'Base_Price']].copy()
        result_df['Scenario'] = scenario_name
        result_df['Shocked_Spot'] = shocked_spot
        result_df['Shocked_Price'] = shocked_prices
        result_df['PnL ($)'] = pnl
        
        return result_df

    def generate_risk_matrix(self, spot_shocks, vol_shocks):
        """
        สร้าง Risk Matrix (ตาราง PnL หลายๆ สถานการณ์) 
        มีประโยชน์มากสำหรับการทำ Heatmap
        """
        results = []
        for s_shock in spot_shocks:
            for v_shock in vol_shocks:
                df = self.apply_scenario(s_shock, v_shock, f"Spot {s_shock*100:+.0f}%, Vol {v_shock*100:+.0f}%")
                
                # หาผลรวม PnL ทั้งพอร์ตในสถานการณ์นี้
                total_pnl = df['PnL ($)'].sum()
                results.append({
                    'Spot_Shock': s_shock,
                    'Vol_Shock': v_shock,
                    'Total_Portfolio_PnL': total_pnl
                })
                
        return pd.DataFrame(results)