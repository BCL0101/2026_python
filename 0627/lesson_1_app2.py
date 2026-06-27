import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4, 1000)

# 第 1 格：sin(pi x)
plt.subplot(221)
plt.plot(x, np.sin(np.pi * x), color='blue', linestyle='-')
plt.title('sin(πx)')

# 第 2 格：cos(pi x)
plt.subplot(222)
plt.plot(x, np.cos(np.pi * x), color='red', linestyle='--')
plt.title('cos(πx)')

# 第 3 格：sin(2pi x)
plt.subplot(223)
plt.plot(x, np.sin(2 * np.pi * x), color='green', linestyle='-.')
plt.title('sin(2πx)')

# 第 4 格：cos(2pi x)
plt.subplot(224)
plt.plot(x, np.cos(2 * np.pi * x), color='magenta', linestyle=':')
plt.title('cos(2πx)')

plt.tight_layout()
plt.show()
