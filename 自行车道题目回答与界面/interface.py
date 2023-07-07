import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from PIL import ImageTk, Image
import matplotlib
matplotlib.use('TkAgg')

# 输入数据
distances = np.array([2.4, 1.5, 2.4, 1.8, 1.8, 2.9, 1.2, 3, 1.2])
widths = np.array([2.9, 2.1, 2.3, 2.1, 1.8, 2.7, 1.5, 2.9, 1.5])

# 线性拟合
coefficients = np.polyfit(distances, widths, 1)
poly_fit = np.poly1d(coefficients)

# 创建主窗口
root = Tk()
root.title("自行车道设计")
root.geometry("600x500")

# 第一个界面
def enter_second_screen():
    second_screen_frame.pack()
    first_screen_frame.pack_forget()

# 第二个界面
def show_curve():
    # 绘制拟合曲线和样本点
    x = np.linspace(distances.min(), distances.max(), 100)
    y = poly_fit(x)

    fig = plt.figure(figsize=(4, 3), dpi=100)
    plt.scatter(distances, widths, label='Sample Points')
    plt.plot(x, y, color='red', label='Linear Fit')
    plt.xlabel('Distance (m)', fontsize=12)
    plt.ylabel('Width (m)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("curve.png")

    curve_image = ImageTk.PhotoImage(Image.open("curve.png"))
    curve_label.config(image=curve_image)
    curve_label.image = curve_image

def calculate_minimum_width():
    # 计算自行车道宽度的最小值
    min_distance = 1.8
    min_width = poly_fit(min_distance)
    minimum_value_label.config(text="Minimum width of the bike lane: {:.2f} m".format(min_width), font=("Arial", 14))

# 第一个界面的框架
first_screen_frame = Frame(root)
first_screen_frame.pack(pady=50)

name_label = Label(first_screen_frame, text="姓名：XXX", font=("Arial", 16))
name_label.pack()

college_label = Label(first_screen_frame, text="学院：XXX", font=("Arial", 16))
college_label.pack()

student_id_label = Label(first_screen_frame, text="学号：XXX", font=("Arial", 16))
student_id_label.pack()

enter_button = Button(first_screen_frame, text="进入", command=enter_second_screen, font=("Arial", 16))
enter_button.pack()

# 第二个界面的框架
second_screen_frame = Frame(root)

title_label = Label(second_screen_frame, text="自行车道的设计", font=("Arial", 18))
title_label.pack(pady=20)

curve_button = Button(second_screen_frame, text="曲线", command=show_curve, font=("Arial", 16))
curve_button.pack()

curve_label = Label(second_screen_frame)
curve_label.pack()

minimum_value_button = Button(second_screen_frame, text="最小值", command=calculate_minimum_width, font=("Arial", 12))
minimum_value_button.pack()

minimum_value_label = Label(second_screen_frame)
minimum_value_label.pack(pady=10)

second_screen_frame.pack_forget()

root.mainloop()
