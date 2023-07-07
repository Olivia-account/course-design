import numpy as np
import matplotlib.pyplot as plt

# 输入数据
distances = np.array([2.4, 1.5, 2.4, 1.8, 1.8, 2.9, 1.2, 3, 1.2])
widths = np.array([2.9, 2.1, 2.3, 2.1, 1.8, 2.7, 1.5, 2.9, 1.5])

# 线性拟合
coefficients = np.polyfit(distances, widths, 1)
poly_fit = np.poly1d(coefficients)

# 绘制拟合曲线和样本点
x = np.linspace(distances.min(), distances.max(), 100)
y = poly_fit(x)

plt.scatter(distances, widths, label='Sample Points')
plt.plot(x, y, color='red', label='Linear Fit')
plt.xlabel('Distance (m)')
plt.ylabel('Width (m)')
plt.legend()
plt.grid(True)
plt.show()

# 计算自行车道宽度的最小值
min_distance = 1.8
min_width = poly_fit(min_distance)

print("Minimum width of the bike lane: {:.2f} m".format(min_width))
