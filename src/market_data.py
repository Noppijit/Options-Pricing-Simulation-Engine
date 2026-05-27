import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np

class MarketDataFeed:
    """คลาสสำหรับดึงข้อมูลราคาหุ้นและ Option จาก Yahoo Finance"""
    
    @staticmethod
    def get_portfolio_options(tickers_list):
        """ดึงข้อมูล Options ของหุ้นหลายๆ ตัวพร้อมกัน พร้อมระบบ Fallback ป้องกันเว็บพัง"""
        all_options = []
        
        for ticker in tickers_list:
            stock = yf.Ticker(ticker)
            
            try:
                # 1. พยายามดึงข้อมูลจริงจากตลาด
                hist = stock.history(period="1d")
                if hist.empty:
                    continue
                spot_price = hist['Close'].iloc[-1]
                
                expirations = stock.options
                if not expirations:
                    continue
                    
                nearest_expiry = expirations[0] 
                opt_chain = stock.option_chain(nearest_expiry)
                
                expiry_date = datetime.strptime(nearest_expiry, '%Y-%m-%d')
                T = max((expiry_date - datetime.now()).days / 365.0, 0.0027)
                
                calls = opt_chain.calls.copy()
                calls['Ticker'] = ticker
                calls['Spot'] = spot_price
                calls['T'] = T
                
                all_options.append(calls)
                
            except Exception as e:
                # 2. ระบบ Fallback: หากโดน Yahoo บล็อค (Rate Limit) ให้สร้างข้อมูลจำลองแทน
                print(f"⚠️ Yahoo Finance บล็อคการดึงข้อมูล {ticker}: {e}")
                mock_calls = MarketDataFeed._generate_mock_options(ticker)
                all_options.append(mock_calls)
            
        if not all_options:
            return None
            
        portfolio_df = pd.concat(all_options, ignore_index=True)
        portfolio_df = portfolio_df[portfolio_df['impliedVolatility'] > 0]
        return portfolio_df

    @staticmethod
    def _generate_mock_options(ticker):
        """สร้างข้อมูล Options จำลองเสมือนจริง เพื่อโชว์ใน Portfolio กรณี API ล่ม"""
        # ล็อก seed ให้ผลลัพธ์คงที่ตามชื่อหุ้น
        np.random.seed(abs(hash(ticker)) % 10000) 
        spot = np.random.uniform(100, 300)
        strikes = np.linspace(spot * 0.8, spot * 1.2, 20) # สร้าง Strike 20 ระดับ
        
        return pd.DataFrame({
            'strike': strikes,
            'lastPrice': np.maximum(spot - strikes, 0) + np.random.uniform(0.5, 3.0, 20),
            'impliedVolatility': np.random.uniform(0.15, 0.50, 20),
            'Ticker': ticker + " (Mock)", # เติมคำว่า Mock ให้รู้ว่าเป็นข้อมูลจำลอง
            'Spot': spot,
            'T': 30 / 365.0 # สมมติว่าเหลือ 30 วันหมดอายุ
        })
    
    @staticmethod
    def get_volatility_surface(ticker, max_expirations=5):
        """ดึงข้อมูล Options หลายๆ วันหมดอายุ เพื่อสร้าง 3D Volatility Surface"""
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            
            if not expirations:
                return None
                
            surface_data = []
            # กวาดข้อมูล 5 วันหมดอายุแรก (เพื่อความรวดเร็ว)
            for exp in expirations[:max_expirations]:
                opt = stock.option_chain(exp)
                calls = opt.calls
                
                expiry_date = datetime.strptime(exp, '%Y-%m-%d')
                T = max((expiry_date - datetime.now()).days / 365.0, 0.0027)
                
                calls['T'] = T
                surface_data.append(calls[['strike', 'T', 'impliedVolatility']])
                
            df = pd.concat(surface_data, ignore_index=True)
            return df[df['impliedVolatility'] > 0] # กรองค่าที่ผิดปกติออก
            
        except Exception as e:
            print(f"⚠️ ใช้ข้อมูลจำลองสำหรับ 3D Surface เนื่องจาก: {e}")
            # ระบบ Fallback จำลองพื้นผิว 3 มิติ (Volatility Smile)
            import numpy as np
            strikes = np.linspace(80, 120, 20)
            times = np.linspace(0.1, 2.0, 5)
            S_grid, T_grid = np.meshgrid(strikes, times)
            
            # สร้างสมการรอยยิ้ม (Strike ไกลๆ Vol จะสูงขึ้น)
            IV_grid = 0.15 + 0.0005 * (S_grid - 100)**2 + 0.02 * T_grid
            
            return pd.DataFrame({
                'strike': S_grid.flatten(),
                'T': T_grid.flatten(),
                'impliedVolatility': IV_grid.flatten()
            })