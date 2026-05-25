import numpy as np
from scipy.stats import norm

class BlackScholesPricer:
    """
    คลาสสำหรับคำนวณราคา Option และค่า Greeks ด้วยโมเดล Black-Scholes
    """
    def __init__(self, S, K, T, r, sigma):
        self.S = float(S)          # Spot Price
        self.K = float(K)          # Strike Price
        self.T = float(T)          # Time to Maturity (Years)
        self.r = float(r)          # Risk-free Rate
        self.sigma = float(sigma)  # Volatility
        
        # คำนวณ d1 และ d2 ล่วงหน้าเพื่อลดความซ้ำซ้อนในการคำนวณ
        self.d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

    def call_price(self):
        """คำนวณราคา Call Option"""
        return self.S * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)

    def put_price(self):
        """คำนวณราคา Put Option"""
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S * norm.cdf(-self.d1)

    def delta(self, option_type='call'):
        """อัตราการเปลี่ยนแปลงของราคา Option ต่อราคาสินทรัพย์อ้างอิง"""
        if option_type.lower() == 'call':
            return norm.cdf(self.d1)
        elif option_type.lower() == 'put':
            return norm.cdf(self.d1) - 1
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def gamma(self):
        """อัตราการเปลี่ยนแปลงของ Delta ต่อราคาสินทรัพย์อ้างอิง"""
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        """ความไวของราคา Option ต่อความผันผวน (Volatility)"""
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T)

    def theta(self, option_type='call'):
        """ความเสื่อมมูลค่าของ Option ตามเวลาที่ผ่านไป (Time Decay)"""
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        if option_type.lower() == 'call':
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
            return term1 - term2
        elif option_type.lower() == 'put':
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
            return term1 + term2
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def get_all_metrics(self, option_type='call'):
        """ดึงค่าทั้งหมดออกมาเป็น Dictionary เพื่อนำไปใช้งานต่อได้ง่าย"""
        if option_type.lower() == 'call':
            price = self.call_price()
        else:
            price = self.put_price()
            
        return {
            "Price": price,
            "Delta": self.delta(option_type),
            "Gamma": self.gamma(),
            "Vega": self.vega(),
            "Theta": self.theta(option_type)
        }