from src.market_data import MarketDataFeed
from src.advanced_models import AdvancedPricer

def main():
    print("=== ดึงข้อมูล Options ของจริงจากตลาด (Live Data) ===")
    
    # 1. กำหนดชื่อหุ้น (ตัวอย่าง: AAPL)
    symbol = "AAPL"
    data_feed = MarketDataFeed(symbol)
    
    # 2. ดึงราคาปัจจุบัน
    spot_price = data_feed.get_spot_price()
    if spot_price is None:
        print("ไม่สามารถดึงข้อมูลราคาหุ้นได้")
        return
        
    print(f"ราคาหุ้น {symbol} ปัจจุบัน: ${spot_price:.2f}")
    
    # 3. ดึงกระดาน Options
    opt_data = data_feed.get_options_data()
    if opt_data:
        T = opt_data['T']
        r = 0.05 # สมมติดอกเบี้ยไร้ความเสี่ยง 5%
        
        # เลือกดู Call Options ของจริง 5 แถวแรก
        calls = opt_data['calls'].head(5)
        
        print("\n=== วิเคราะห์ Implied Volatility (IV) ===")
        print(f"{'Strike':<10} | {'Market Price':<15} | {'IV (Yahoo)':<15} | {'IV (Our Engine)':<15}")
        print("-" * 60)
        
        for index, row in calls.iterrows():
            K = row['strike']
            market_price = row['lastPrice']
            yahoo_iv = row['impliedVolatility']
            
            # คำนวณ IV ด้วย Engine ของเรา
            our_iv = AdvancedPricer.implied_volatility(
                market_price=market_price, 
                S=spot_price, 
                K=K, 
                T=T, 
                r=r, 
                option_type='call'
            )
            
            print(f"{K:<10.2f} | ${market_price:<14.2f} | {yahoo_iv*100:>8.2f}%      | {our_iv*100:>8.2f}%")

if __name__ == "__main__":
    main()