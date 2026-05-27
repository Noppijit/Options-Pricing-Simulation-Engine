import yfinance as yf
import pandas as pd
from datetime import datetime

class MarketDataFeed:
    """คลาสสำหรับดึงข้อมูลราคาหุ้นและ Option จาก Yahoo Finance"""
    
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.stock = yf.Ticker(ticker_symbol)
        
    def get_spot_price(self):
        """ดึงราคาหุ้นปัจจุบัน"""
        data = self.stock.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
        
    def get_options_data(self):
        """ดึงข้อมูล Options ทั้งหมดของหุ้นตัวนี้"""
        # ดูวันที่หมดอายุทั้งหมดที่มีให้เทรด
        expirations = self.stock.options
        if not expirations:
            print("ไม่พบข้อมูล Options สำหรับหุ้นตัวนี้")
            return None
            
        # เลือกวันหมดอายุที่ใกล้ที่สุด
        nearest_expiry = expirations[0]
        opt_chain = self.stock.option_chain(nearest_expiry)
        
        # คำนวณ Time to Maturity (T) เป็นหน่วยปี
        expiry_date = datetime.strptime(nearest_expiry, '%Y-%m-%d')
        days_to_expiry = (expiry_date - datetime.now()).days
        # ป้องกันกรณีหมดอายุวันนี้ (T=0) จะคำนวณ BSM ไม่ได้
        T = max(days_to_expiry / 365.0, 0.0027) # ให้ขั้นต่ำคือ 1 วัน
        
        print(f"ดึงข้อมูล {self.ticker_symbol} หมดอายุวันที่ {nearest_expiry} (T = {T:.4f} ปี)")
        
        return {
            'T': T,
            'calls': opt_chain.calls,
            'puts': opt_chain.puts
        }
    
    @staticmethod
    def get_portfolio_options(tickers_list):
        """ดึงข้อมูล Options ของหุ้นหลายๆ ตัวพร้อมกัน แล้วมัดรวมเป็น DataFrame เดียว"""
        all_options = []
        
        for ticker in tickers_list:
            stock = yf.Ticker(ticker)
            
            # ดึงราคา Spot
            hist = stock.history(period="1d")
            if hist.empty:
                continue
            spot_price = hist['Close'].iloc[-1]
            
            # ดึงวันหมดอายุ
            expirations = stock.options
            if not expirations:
                continue
                
            nearest_expiry = expirations[0] # เอาซีรีส์ที่ใกล้หมดอายุที่สุด
            opt_chain = stock.option_chain(nearest_expiry)
            
            # คำนวณ Time to Maturity (T)
            expiry_date = datetime.strptime(nearest_expiry, '%Y-%m-%d')
            T = max((expiry_date - datetime.now()).days / 365.0, 0.0027)
            
            # เอาเฉพาะ Call Options มาวิเคราะห์
            calls = opt_chain.calls.copy()
            calls['Ticker'] = ticker
            calls['Spot'] = spot_price
            calls['T'] = T
            
            all_options.append(calls)
            
        if not all_options:
            return None
            
        # รวม DataFrame ของทุกหุ้นเข้าด้วยกัน
        portfolio_df = pd.concat(all_options, ignore_index=True)
        
        # กรองเอาเฉพาะข้อมูลที่มี Volatility มากกว่า 0 เพื่อป้องกัน Error
        portfolio_df = portfolio_df[portfolio_df['impliedVolatility'] > 0]
        return portfolio_df