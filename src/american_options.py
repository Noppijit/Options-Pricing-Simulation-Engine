import numpy as np

class AmericanOptionLSM:
    """
    ประเมินราคา American Options ด้วยวิธี Longstaff-Schwartz (Least Squares Monte Carlo)
    """
    def __init__(self, S, K, T, r, sigma, num_paths=10000, num_steps=50):
        self.S = float(S)
        self.K = float(K)
        self.T = float(T)
        self.r = float(r)
        self.sigma = float(sigma)
        self.num_paths = int(num_paths)
        self.num_steps = int(num_steps)

    def price(self, option_type='put'):
        np.random.seed(42) # ล็อกผลลัพธ์
        dt = self.T / self.num_steps
        discount = np.exp(-self.r * dt)
        
        # 1. จำลองเส้นทางราคา (GBM Paths)
        Z = np.random.standard_normal((self.num_steps, self.num_paths))
        S_paths = np.zeros((self.num_steps + 1, self.num_paths))
        S_paths[0] = self.S
        
        for t in range(1, self.num_steps + 1):
            S_paths[t] = S_paths[t-1] * np.exp((self.r - 0.5 * self.sigma**2) * dt + 
                                               self.sigma * np.sqrt(dt) * Z[t-1])
                                               
        # 2. คำนวณ Payoff ณ วันหมดอายุ (T)
        if option_type.lower() == 'call':
            cash_flow = np.maximum(S_paths[-1] - self.K, 0)
        else:
            cash_flow = np.maximum(self.K - S_paths[-1], 0)
            
        # 3. ถอยหลังเวลา (Backward Induction) เพื่อหาจุดใช้สิทธิ์ก่อนกำหนด
        for t in range(self.num_steps - 1, 0, -1):
            # หาสถานะ In-the-money (ITM) ณ เวลา t
            if option_type.lower() == 'call':
                itm = np.where(S_paths[t] > self.K)[0]
                exercise_val = S_paths[t, itm] - self.K
            else:
                itm = np.where(S_paths[t] < self.K)[0]
                exercise_val = self.K - S_paths[t, itm]
                
            # ถ้ามีเส้นทางที่สามารถทำกำไรได้
            if len(itm) > 0:
                # คิดลดกระแสเงินสดอนาคตมาที่เวลา t
                discounted_cf = cash_flow[itm] * discount
                
                # ทำ Regression (Polynomial Degree 2) เพื่อหามูลค่าการถือต่อ
                X = S_paths[t, itm]
                poly_coeffs = np.polyfit(X, discounted_cf, 2)
                continuation_val = np.polyval(poly_coeffs, X)
                
                # ตัดสินใจ: ใช้สิทธิ์ทันที > มูลค่าคาดหวังถ้าถือต่อ หรือไม่?
                exercise_now = exercise_val > continuation_val
                
                # คิดลดกระแสเงินสดของทุกเส้นทางลง 1 สเต็ปก่อน
                cash_flow *= discount
                
                # อัปเดตกระแสเงินสดเฉพาะเส้นทางที่เลือก "ใช้สิทธิ์ก่อนกำหนด"
                cash_flow[itm[exercise_now]] = exercise_val[exercise_now]
            else:
                # ถ้าไม่มีใคร ITM เลย ก็แค่คิดลดเวลาเฉยๆ
                cash_flow *= discount
                
        # 4. คิดลดกลับมาที่เวลาปัจจุบัน (t=0)
        option_price = np.mean(cash_flow) * discount
        return option_price