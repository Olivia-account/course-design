import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 导入字体管理器
from matplotlib.font_manager import FontProperties

# 设置中文显示
font = FontProperties(fname='C:/Windows/Fonts/SimHei.ttf')  # 替换为你实际安装的SimHei字体路径
plt.rcParams['font.family'] = font.get_name()

# 从Excel文件加载数据
data = pd.read_excel('新书热卖榜.xlsx')

# 选择用于回归分析的相关列
columns = ['评论数', '推荐度', '扣价', '原价', '扣率']

# 删除包含缺失值的行
data = data.dropna(subset=columns)

# 将选定的列转换为数值类型
data[columns] = data[columns].apply(pd.to_numeric)

# 执行多元回归分析
X = data[columns]
X = np.c_[np.ones(len(X)), X]  # 添加一列全为1的向量作为截距
y = data['排名']

coefficients, residuals, _, _ = np.linalg.lstsq(X, y, rcond=None)

# 打印回归系数
print('回归系数:')
for i, column in enumerate(['截距'] + columns):
    print(f'{column}: {coefficients[i]:.2f}')


# Generate a scatter plot of actual ranks vs. predicted ranks
predicted_ranks = X @ coefficients
plt.scatter(data.index, data['排名'], label='Actual Ranks', alpha=0.5)
plt.plot(data.index, predicted_ranks, color='red', label='Predicted Ranks')
plt.xlabel('Index')
plt.ylabel('Rank')
plt.legend()
plt.title('Actual vs. Predicted Ranks')
plt.savefig('Actual vs. Predicted Ranks.png')
plt.show()

# Generate a bar chart of the coefficients
plt.bar(['Intercept'] + columns, coefficients)
plt.xlabel('Variable')
plt.ylabel('Coefficient')
plt.title('Regression Coefficients')
plt.savefig('Regression Coefficients.png')
plt.show()