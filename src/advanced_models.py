import numpy as np
from src.black_scholes import BlackScholesPricer

class AdvancedPricer:
    """คลาสสำหรับโมเดลคณิตศาสตร์ขั้นสูง (Implied Volatility)"""
    
    @staticmethod
    def implied_volatility(market_price, S, K, T, r, option_type='call', tol=1e-5, max_iter=100):
        """
        คำนวณหา Implied Volatility ด้วย Newton-Raphson Method
        """
        # สุ่มเดาค่าความผันผวนเริ่มต้นที่ 20%
        sigma = 0.20  
        
        for i in range(max_iter):
            # สร้าง Object BSM ด้วยค่า sigma ปัจจุบัน
            pricer = BlackScholesPricer(S, K, T, r, sigma)
            
            # คำนวณราคาและ Vega
            if option_type.lower() == 'call':
                price = pricer.call_price()
            else:
                price = pricer.put_price()
                
            vega = pricer.vega()
            
            # หาความคลาดเคลื่อน (ส่วนต่างระหว่างราคาคำนวณกับราคาตลาด)
            diff = price - market_price
            
            # ถ้าคลาดเคลื่อนน้อยกว่าค่า Tolereance (tol) ถือว่าเจอคำตอบแล้ว
            if abs(diff) < tol:
                return sigma
                
            # ป้องกันกรณี Vega เข้าใกล้ 0 ซึ่งจะทำให้หารด้วยศูนย์
            if vega < 1e-4:
                return np.nan
                
            # อัปเดตค่า sigma ใหม่ด้วยสูตร Newton-Raphson
            sigma = sigma - (diff / vega)
            
            # ป้องกันไม่ให้ค่า sigma ติดลบ
            if sigma <= 0:
                sigma = 0.01
                
        return np.nan # ถ้าวนลูปจนครบกำหนดแล้วยังไม่เจอคำตอบ