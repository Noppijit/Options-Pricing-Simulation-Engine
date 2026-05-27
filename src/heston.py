import numpy as np

class HestonMonteCarlo:
    """คลาสสำหรับจำลองราคาด้วย Heston Stochastic Volatility Model"""
    
    def __init__(self, S0, v0, kappa, theta, xi, rho, r, T, num_steps=252, num_paths=10000):
        self.S0 = float(S0)          # ราคาปัจจุบัน
        self.v0 = float(v0)          # ความแปรปรวนปัจจุบัน (Variance = Volatility^2)
        self.kappa = float(kappa)    # Speed of mean reversion
        self.theta = float(theta)    # Long-term variance
        self.xi = float(xi)          # Volatility of volatility
        self.rho = float(rho)        # Correlation ระหว่างราคาและความผันผวน
        self.r = float(r)            # Risk-free rate
        self.T = float(T)            # Time to maturity
        self.num_steps = int(num_steps)
        self.num_paths = int(num_paths)
        
    def simulate_paths(self):
        """จำลองเส้นทางราคาและความผันผวนด้วยวิธี Euler-Maruyama"""
        np.random.seed(42) # ล็อกผลลัพธ์
        dt = self.T / self.num_steps
        
        # สร้าง Array เปล่าสำหรับเก็บราคากับความผันผวน
        S = np.zeros((self.num_paths, self.num_steps + 1))
        v = np.zeros((self.num_paths, self.num_steps + 1))
        
        # กำหนดค่าเริ่มต้น (t=0)
        S[:, 0] = self.S0
        v[:, 0] = self.v0
        
        for t in range(1, self.num_steps + 1):
            # 1. สร้างตัวแปรสุ่ม 2 ตัวที่เป็นอิสระต่อกัน (Z1, Z2)
            Z1 = np.random.standard_normal(self.num_paths)
            Z2 = np.random.standard_normal(self.num_paths)
            
            # 2. ผสม Z1 และ Z2 เพื่อสร้างตัวแปรสุ่มที่มีความสัมพันธ์กันตามค่า rho (Cholesky Decomposition)
            Z_S = Z1
            Z_v = self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2
            
            # 3. จัดการกรณี Variance ติดลบ (Full Truncation Scheme)
            # เนื่องจากในคอมพิวเตอร์อาจเกิดข้อผิดพลาดในการปัดเศษจนติดลบได้ เราจึงบังคับให้ขั้นต่ำเป็น 0
            v_t_minus_1 = np.maximum(v[:, t-1], 0)
            
            # 4. อัปเดตราคาหุ้น (S) แบบ Geometric Brownian Motion ที่เปลี่ยนค่า vol
            S[:, t] = S[:, t-1] * np.exp((self.r - 0.5 * v_t_minus_1) * dt + 
                                         np.sqrt(v_t_minus_1 * dt) * Z_S)
            
            # 5. อัปเดตความผันผวน (v) ตามกระบวนการ Mean-Reverting Square Root Process
            v[:, t] = v[:, t-1] + self.kappa * (self.theta - v_t_minus_1) * dt + \
                      self.xi * np.sqrt(v_t_minus_1 * dt) * Z_v
                      
            # บังคับค่าความผันผวนใหม่ไม่ให้ติดลบ (เพื่อใช้ในรอบถัดไป)
            v[:, t] = np.maximum(v[:, t], 0)
            
        return S, v

    def calculate_option_price(self, K, option_type='call'):
        """คำนวณราคา Option จากเส้นทางที่จำลองได้"""
        S_paths, _ = self.simulate_paths()
        terminal_prices = S_paths[:, -1] # ดึงราคา ณ วันหมดอายุ
        
        if option_type.lower() == 'call':
            payoffs = np.maximum(terminal_prices - K, 0)
        elif option_type.lower() == 'put':
            payoffs = np.maximum(K - terminal_prices, 0)
            
        discount_factor = np.exp(-self.r * self.T)
        return np.mean(payoffs) * discount_factor