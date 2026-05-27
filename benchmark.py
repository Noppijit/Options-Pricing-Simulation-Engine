import numpy as np
import pandas as pd
import time
from src.black_scholes import BlackScholesPricer
from src.vectorized_engine import VectorizedPricer

def generate_mock_portfolio(num_options):
    """สุ่มสร้างข้อมูล Options ขึ้นมาทดสอบ"""
    print(f"กำลังสร้างข้อมูลจำลองจำนวน {num_options:,} ตัว...")
    np.random.seed(42)
    return pd.DataFrame({
        'Spot': np.random.uniform(50, 150, num_options),
        'Strike': np.random.uniform(50, 150, num_options),
        'Time': np.random.uniform(0.1, 3.0, num_options),
        'Rate': np.random.uniform(0.01, 0.05, num_options),
        'Volatility': np.random.uniform(0.1, 0.5, num_options)
    })

def test_performance():
    # 1. กำหนดจำนวน Options ที่ต้องการเทส (1 ล้านตัว)
    NUM_OPTIONS = 1_000_000 
    df = generate_mock_portfolio(NUM_OPTIONS)
    print("-" * 50)
    
    # ---------------------------------------------------------
    # การทดสอบที่ 1: Vectorized Engine (คำนวณรวดเดียวผ่าน NumPy)
    # ---------------------------------------------------------
    print("เริ่มทดสอบวิธีที่ 1: Vectorized Engine (NumPy Arrays)...")
    start_time_vec = time.time()
    
    # ส่งข้อมูลเป็น Series เข้าไปคำนวณรวดเดียว
    df['Call_Price_Vec'] = VectorizedPricer.black_scholes_batch(
        df['Spot'], df['Strike'], df['Time'], df['Rate'], df['Volatility'], 'call'
    )
    
    end_time_vec = time.time()
    vec_duration = end_time_vec - start_time_vec
    print(f"✅ Vectorized ใช้เวลา: {vec_duration:.4f} วินาที")
    
    # ---------------------------------------------------------
    # การทดสอบที่ 2: For Loop (วิธียอดฮิตของมือใหม่)
    # ---------------------------------------------------------
    # ลดจำนวนลงเหลือแค่ 10,000 ตัว ไม่งั้น Loop 1 ล้านตัวจะรอนานเกินไป
    SMALL_SAMPLE = 10000 
    df_small = df.head(SMALL_SAMPLE).copy()
    
    print(f"\nเริ่มทดสอบวิธีที่ 2: For Loop แบบดั้งเดิม (ทดสอบแค่ {SMALL_SAMPLE:,} ตัว)...")
    start_time_loop = time.time()
    
    loop_prices = []
    for _, row in df_small.iterrows():
        # เรียกใช้ Class เก่าที่เราเขียนไว้ตอนแรก
        pricer = BlackScholesPricer(row['Spot'], row['Strike'], row['Time'], row['Rate'], row['Volatility'])
        loop_prices.append(pricer.call_price())
        
    end_time_loop = time.time()
    loop_duration = end_time_loop - start_time_loop
    print(f"✅ For Loop ใช้เวลา: {loop_duration:.4f} วินาที (เฉพาะ {SMALL_SAMPLE:,} ตัว)")
    
    # ---------------------------------------------------------
    # สรุปผลลัพธ์ (Extrapolate เพื่อเปรียบเทียบ)
    # ---------------------------------------------------------
    print("-" * 50)
    print("📊 สรุปผลการทดสอบประสิทธิภาพ (Performance Report)")
    print("-" * 50)
    
    # คำนวณว่าถ้า Loop ทำ 1 ล้านตัวจะใช้เวลาเท่าไหร่
    estimated_loop_total = loop_duration * (NUM_OPTIONS / SMALL_SAMPLE)
    speedup_factor = estimated_loop_total / vec_duration
    
    print(f"จำนวน Options: {NUM_OPTIONS:,} สัญญา")
    print(f"เวลาที่คาดหวังถ้าใช้ For Loop:  ~{estimated_loop_total:.2f} วินาที")
    print(f"เวลาที่ใช้จริงของ Vectorized: {vec_duration:.4f} วินาที")
    print(f"🚀 ความเร็วเพิ่มขึ้น (Speedup): เร็วขึ้น {speedup_factor:,.0f} เท่า!")
    
    # แสดงตัวอย่างข้อมูลที่คำนวณเสร็จแล้ว
    print("\nตัวอย่างข้อมูลใน Portfolio หลังจากคำนวณเสร็จ:")
    print(df[['Spot', 'Strike', 'Volatility', 'Call_Price_Vec']].head())

if __name__ == "__main__":
    test_performance()