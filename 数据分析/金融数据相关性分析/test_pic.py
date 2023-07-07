# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 读取Excel文件
data = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 提取"从业人员"、"实收资本"和"贷款余额"这三列的数据
employees = data['从业人员']
capital = data['实收资本']
loan_balance = data['贷款余额']

# 计算相关性系数和p值
correlation, p_value = pearsonr(employees, capital)
print("从业人员和实收资本之间的相关性系数：", correlation)
print("p值：", p_value)

correlation, p_value = pearsonr(employees, loan_balance)
print("从业人员和贷款余额之间的相关性系数：", correlation)
print("p值：", p_value)

correlation, p_value = pearsonr(capital, loan_balance)
print("实收资本和贷款余额之间的相关性系数：", correlation)
print("p值：", p_value)

# 绘制散点图
plt.scatter(employees, capital)
plt.xlabel('employees')
plt.ylabel('capital')
plt.title('Correlation')
plt.savefig('从业人员与实收资本的相关性.jpg')
plt.show()
# 绘制散点图
plt.scatter(capital, loan_balance)
plt.xlabel('capital')
plt.ylabel('loan_balance')
plt.title('Correlation')
plt.savefig('实收资本与贷款余额的相关性.jpg')
plt.show()
# 绘制散点图
plt.scatter(employees, loan_balance)
plt.xlabel('employees')
plt.ylabel('loan_balance')
plt.title('Correlation')
plt.savefig('从业人员与贷款余额的相关性.jpg')
plt.show()
