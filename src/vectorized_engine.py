import numpy as np
import pandas as pd
from scipy.stats import norm

class VectorizedPricer:
    """
    เครื่องยนต์คำนวณ Options ทีละหลายหมื่นตัวพร้อมกัน (Batch Processing) 
    โดยใช้เทคนิค Vectorization ของ NumPy เพื่อประสิทธิภาพสูงสุด
    """
    
    @staticmethod
    def black_scholes_batch(S, K, T, r, sigma, option_type='call'):
        """
        รับค่าพารามิเตอร์ที่เป็น NumPy Array (หรือ Pandas Series) และคืนค่า Array ของราคา
        """
        # ป้องกันกรณี T = 0 เพื่อไม่ให้เกิด Error หารด้วยศูนย์
        T = np.maximum(T, 1e-5) 
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            prices = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == 'put':
            prices = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("option_type ต้องเป็น 'call' หรือ 'put'")
            
        return prices

    @staticmethod
    def greeks_batch(S, K, T, r, sigma, option_type='call'):
        """
        คำนวณค่า Greeks สำหรับ Options ทั้งพอร์ตโฟลิโอในครั้งเดียว
        """
        T = np.maximum(T, 1e-5)
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # คืนค่าเป็น Dictionary ของ Array เพื่อนำไปสร้าง DataFrame ต่อได้ง่าย
        deltas = norm.cdf(d1) if option_type == 'call' else norm.cdf(d1) - 1
        gammas = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vegas = S * norm.pdf(d1) * np.sqrt(T)
        
        term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        if option_type == 'call':
            thetas = term1 - r * K * np.exp(-r * T) * norm.cdf(d2)
        else:
            thetas = term1 + r * K * np.exp(-r * T) * norm.cdf(-d2)
            
        return {
            "Delta": deltas,
            "Gamma": gammas,
            "Vega": vegas,
            "Theta": thetas
        }