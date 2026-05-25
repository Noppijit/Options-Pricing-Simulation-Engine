# นำเข้าคลาสต่างๆ ที่เราเขียนไว้ในโฟลเดอร์ src
from src.black_scholes import BlackScholesPricer
from src.simulation import MonteCarloPricer
from src.visualization import OptionVisualizer
import numpy as np

def main():
    print("=== เริ่มต้นทำงาน: Options Pricing & Simulation Engine ===")
    
    # 1. กำหนดพารามิเตอร์ของ Option (คุณสามารถลองเปลี่ยนค่าตัวเลขเหล่านี้ได้)
    params = {
        'S': 100,      # ราคาหุ้นปัจจุบัน (Spot Price)
        'K': 100,      # ราคาใช้สิทธิ (Strike Price)
        'T': 1.0,      # ระยะเวลาจนหมดอายุ (1 ปี)
        'r': 0.05,     # อัตราดอกเบี้ยไร้ความเสี่ยง (5%)
        'sigma': 0.20  # ความผันผวน (20%)
    }
    
    print(f"\n[1] ข้อมูลนำเข้า: Spot={params['S']}, Strike={params['K']}, T={params['T']} ปี, Volatility={params['sigma']*100}%")

    # 2. คำนวณราคาด้วย Black-Scholes Model (พาร์ท 1)
    print("\n[2] กำลังคำนวณด้วย Black-Scholes Model...")
    bs_pricer = BlackScholesPricer(**params)
    bs_metrics = bs_pricer.get_all_metrics(option_type='call')
    
    print(f"  -> ราคา Call Option ทางทฤษฎี: {bs_metrics['Price']:.4f}")
    print(f"  -> ค่าความเสี่ยง (Greeks): Delta={bs_metrics['Delta']:.4f}, Gamma={bs_metrics['Gamma']:.4f}")

    # 3. จำลองเส้นทางด้วย Monte Carlo Simulation (พาร์ท 2)
    # จำลอง 10,000 เส้นทาง เพื่อดูว่าราคาจะใกล้เคียงทฤษฎีแค่ไหน
    print("\n[3] กำลังจำลอง Monte Carlo (10,000 เส้นทาง)...")
    mc_pricer = MonteCarloPricer(**params, num_paths=10000)
    mc_prices = mc_pricer.calculate_prices()
    paths = mc_pricer.simulated_paths # ดึงเส้นทางออกมาเก็บไว้พล็อต
    
    print(f"  -> ราคา Call Option จากการจำลอง: {mc_prices['Monte_Carlo_Call']:.4f}")
    print(f"  -> ความคลาดเคลื่อน (Error): {abs(bs_metrics['Price'] - mc_prices['Monte_Carlo_Call']):.4f}")

    # 4. พล็อตกราฟ (พาร์ท 3)
    print("\n[4] กำลังสร้างกราฟ (Visualization)...")
    viz = OptionVisualizer()
    
    # พล็อต 1: เส้นทางราคาจำลอง
    print("  -> แสดงกราฟ 1: Monte Carlo Paths (คำแนะนำ: ปิดหน้าต่างกราฟแรก เพื่อให้โปรแกรมรันกราฟที่สองต่อ)")
    viz.plot_simulation_paths(paths, params['K'])
    
    # พล็อต 2: ความสัมพันธ์ของ Greeks
    print("  -> แสดงกราฟ 2: Option Greeks Profile")
    S_range = np.linspace(50, 150, 100) # สร้างช่วงราคาตั้งแต่ 50 ถึง 150
    viz.plot_greeks_profile(
        BlackScholesPricer, 
        S_range, 
        K=params['K'], 
        T=params['T'], 
        r=params['r'], 
        sigma=params['sigma']
    )
    
    print("\n=== การทำงานเสร็จสมบูรณ์ ===")

if __name__ == "__main__":
    main()