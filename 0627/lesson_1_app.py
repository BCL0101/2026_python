"""
互動式正弦與餘弦波形繪圖應用程式
使用 numpy 進行數值運算，matplotlib 進行繪圖與互動控制
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（macOS 支援的繁體中文字型）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 建立圖表
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # 預留空間給滑桿

# X 軸範圍：0 到 4π
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數
A_init = 1.0      # 振幅
omega_init = 1.0  # 頻率
phi_init = 0.0    # 相位偏移

# 繪製初始波形
sin_line, = ax.plot(x, A_init * np.sin(omega_init * x + phi_init),
                    label='sin', color='blue', linewidth=2)
cos_line, = ax.plot(x, A_init * np.cos(omega_init * x + phi_init),
                    label='cos', color='red', linewidth=2, linestyle='--')

# 設定圖表屬性
ax.set_title('正弦與餘弦波形')
ax.set_xlabel('x (弧度)')
ax.set_ylabel('y')
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')

# 建立滑桿的座軸
ax_amp = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_freq = plt.axes([0.15, 0.10, 0.65, 0.03])
ax_phase = plt.axes([0.15, 0.05, 0.65, 0.03])

# 建立滑桿
slider_amp = Slider(ax_amp, '振幅 A', 0.1, 5.0, valinit=A_init)
slider_freq = Slider(ax_freq, '頻率 ω', 0.1, 10.0, valinit=omega_init)
slider_phase = Slider(ax_phase, '相位 φ', 0, 2 * np.pi, valinit=phi_init)

# 更新波形的函數
def update(val):
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val
    sin_line.set_ydata(A * np.sin(omega * x + phi))
    cos_line.set_ydata(A * np.cos(omega * x + phi))
    fig.canvas.draw_idle()

# 註冊滑桿事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()
