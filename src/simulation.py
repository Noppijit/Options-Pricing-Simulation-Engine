import numpy as np

class MonteCarloPricer:
    """
    คลาสสำหรับจำลองราคาสินทรัพย์ด้วย Geometric Brownian Motion (GBM) 
    และประเมินราคา Option ด้วย Monte Carlo Simulation
    """
    def __init__(self, S, K, T, r, sigma, num_paths=10000, num_steps=252):
        self.S = float(S)          # Spot Price
        self.K = float(K)          # Strike Price
        self.T = float(T)          # Time to Maturity (Years)
        self.r = float(r)          # Risk-free Rate
        self.sigma = float(sigma)  # Volatility
        self.num_paths = int(num_paths) # จำนวนเส้นทางที่ต้องการจำลอง
        self.num_steps = int(num_steps) # จำนวนสเต็ปเวลา (เช่น 252 วันทำการต่อปี)
        
        # เก็บเส้นทางจำลองไว้ในตัวแปรเพื่อนำไปพล็อตกราฟในพาร์ทถัดไป
        self.simulated_paths = None

    def simulate_paths(self):
        """สร้างเส้นทางราคาสินทรัพย์จำลองด้วย GBM"""
        np.random.seed(42) # ล็อก Seed เพื่อให้ผลลัพธ์คงที่ (สำหรับการนำเสนองาน)
        dt = self.T / self.num_steps
        
        # สุ่มค่า Z จาก Standard Normal Distribution รูปแบบ Matrix (Paths x Steps)
        Z = np.random.standard_normal((self.num_paths, self.num_steps))
        
        # สร้าง Array เก็บราคาทุก Step
        paths = np.zeros((self.num_paths, self.num_steps + 1))
        paths[:, 0] = self.S
        
        # คำนวณราคาในแต่ละ Step ด้วยสมการ GBM
        for t in range(1, self.num_steps + 1):
            drift = (self.r - 0.5 * self.sigma ** 2) * dt
            diffusion = self.sigma * np.sqrt(dt) * Z[:, t-1]
            paths[:, t] = paths[:, t-1] * np.exp(drift + diffusion)
            
        self.simulated_paths = paths
        return self.simulated_paths

    def calculate_prices(self):
        """คำนวณราคา Call และ Put Option จากเส้นทางที่จำลองไว้"""
        if self.simulated_paths is None:
            self.simulate_paths()
            
        # ดึงราคาสินทรัพย์ ณ วันหมดอายุ (Column สุดท้ายของ Matrix)
        terminal_prices = self.simulated_paths[:, -1]
        
        # คำนวณ Payoff: 
        # Call = max(S_T - K, 0)
        # Put = max(K - S_T, 0)
        call_payoffs = np.maximum(terminal_prices - self.K, 0)
        put_payoffs = np.maximum(self.K - terminal_prices, 0)
        
        # หาค่าเฉลี่ย (Expected Payoff) และคิดลดกลับมาเป็นมูลค่าปัจจุบัน (Discounting)
        discount_factor = np.exp(-self.r * self.T)
        call_price = np.mean(call_payoffs) * discount_factor
        put_price = np.mean(put_payoffs) * discount_factor
        
        return {
            "Monte_Carlo_Call": call_price,
            "Monte_Carlo_Put": put_price
        }