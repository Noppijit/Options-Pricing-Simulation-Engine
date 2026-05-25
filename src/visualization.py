import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ตั้งค่าสไตล์ให้ดูสวยงามและเป็นทางการ
plt.style.use('dark_background') 
sns.set_palette("viridis")

class OptionVisualizer:
    """คลาสสำหรับพล็อตกราฟราคา Option และการจำลองทางสถิติ"""
    
    @staticmethod
    def plot_simulation_paths(paths, strike_price):
        """พล็อตเส้นทางราคาหุ้นจากการจำลอง Monte Carlo"""
        plt.figure(figsize=(12, 6))
        # พล็อตเพียง 100 เส้นแรกเพื่อไม่ให้กราฟรกเกินไป
        plt.plot(paths[:100, :].T, lw=0.8, alpha=0.6)
        
        # เพิ่มเส้น Strike Price
        plt.axhline(strike_price, color='red', linestyle='--', label=f'Strike Price ({strike_price})')
        
        plt.title('Monte Carlo Simulation: Asset Price Paths (Geometric Brownian Motion)', fontsize=14)
        plt.xlabel('Time Steps (Days)', fontsize=12)
        plt.ylabel('Asset Price', fontsize=12)
        plt.legend()
        plt.grid(alpha=0.2)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_greeks_profile(pricer_class, S_range, K, T, r, sigma, option_type='call'):
        """พล็อตความสัมพันธ์ระหว่าง Spot Price กับค่า Greeks ต่างๆ"""
        deltas, gammas, vegas, thetas = [], [], [], []
        
        for s in S_range:
            p = pricer_class(s, K, T, r, sigma)
            deltas.append(p.delta(option_type))
            gammas.append(p.gamma())
            vegas.append(p.vega())
            thetas.append(p.theta(option_type))
            
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Option Greeks Profile ({option_type.capitalize()})', fontsize=16)

        # Delta
        axes[0, 0].plot(S_range, deltas, color='cyan')
        axes[0, 0].set_title('Delta (Price Sensitivity)')
        axes[0, 0].grid(alpha=0.3)

        # Gamma
        axes[0, 1].plot(S_range, gammas, color='magenta')
        axes[0, 1].set_title('Gamma (Delta Sensitivity)')
        axes[0, 1].grid(alpha=0.3)

        # Vega
        axes[1, 0].plot(S_range, vegas, color='yellow')
        axes[1, 0].set_title('Vega (Volatility Sensitivity)')
        axes[1, 0].grid(alpha=0.3)

        # Theta
        axes[1, 1].plot(S_range, thetas, color='orange')
        axes[1, 1].set_title('Theta (Time Decay)')
        axes[1, 1].grid(alpha=0.3)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()