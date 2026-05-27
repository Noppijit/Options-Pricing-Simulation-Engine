from src.heston import HestonMonteCarlo

def main():
    print("=== ทดสอบ Heston Stochastic Volatility Model ===")
    
    # พารามิเตอร์พื้นฐาน
    S0 = 100
    K = 100
    T = 1.0
    r = 0.05
    
    # พารามิเตอร์เฉพาะของ Heston
    v0 = 0.04      # ความแปรปรวนเริ่มต้น (เทียบเท่า Volatility 20%)
    kappa = 2.0    # ความเร็วในการกลับสู่ค่าเฉลี่ย
    theta = 0.04   # ค่าเฉลี่ยระยะยาว
    xi = 0.1       # Vol of vol
    rho = -0.7     # ตลาดหุ้นจริงมักมี Leverage Effect ติดลบ (หุ้นตก=volพุ่ง)
    
    print("กำลังจำลองเส้นทาง (10,000 Paths)...")
    heston_model = HestonMonteCarlo(S0, v0, kappa, theta, xi, rho, r, T, num_paths=10000)
    
    # คำนวณราคา Call Option
    call_price = heston_model.calculate_option_price(K, option_type='call')
    put_price = heston_model.calculate_option_price(K, option_type='put')
    
    print(f"\nราคา Call Option (Heston Model): ${call_price:.4f}")
    print(f"ราคา Put Option (Heston Model):  ${put_price:.4f}")

if __name__ == "__main__":
    main()