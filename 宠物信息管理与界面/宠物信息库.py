import tkinter as tk
from tkinter import messagebox
import csv

# 创建一个空字典用于存储数据
data_dict = {}
status_li = [0,0,0,0,0,0]

# 读取csv文件中的数据
def read_csv():
    try:
        with open('pet111.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                number = row[0]
                name = row[1]
                type = row[2]
                age = row[3]
                info = row[4]
                notice = row[5]
                YL = row[6]
                MR = row[7]
                data_dict[number] = {
                    "name": name,
                    "number": number,
                    "type": type,
                    "age": age,
                    "info": info,
                    "notice": notice,
                    "YL": YL,   # 初始化宠物美容费用为0
                    "MR": YL  # 初始化宠物治疗费用为0
                }
    except FileNotFoundError:
        pass

# 定义按钮点击事件，将数据添加到字典中
def submit():
    name = name_entry.get()
    number = number_entry.get()
    type = type_entry.get()
    age = age_entry.get()
    info = info_entry.get()
    notice = notice_entry.get()
    YL = YL_entry.get()
    MR = MR_entry.get()
    data_dict[number] = {
        "name": name,
        "number": number,
        "type": type,
        "age": age,
        "info": info,
        "notice": notice,
        "YL": YL,
        "MR": MR
    }
    write_csv()  # try
    # 清空输入框中的文本内容
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    info_entry.delete(0, tk.END)
    notice_entry.delete(0, tk.END)


# 定义按钮点击事件，显示所有数据
def show_data():
    # 创建一个新窗口用于显示数据
    data_window = tk.Toplevel(root)
    data_window.geometry("1000x600")
    data_window.title("宠物资料库")
    # 创建一个框架用于显示数据
    data_frame = tk.Frame(data_window)
    data_frame.grid()
    title_label = tk.Label(
        data_frame, text="编号|宠物昵称|类型|年龄|其他信息|医疗费用|美容费用", font=("simsun", 10), fg="blue")
    title_label.grid(row=0, column=0, sticky="w")
    # 遍历字典中的数据，将其显示在框架中
    n = 1  # 创建一个计数器
    for num, data in data_dict.items():
        data_label = tk.Label(data_frame,
                              text=f"{data['number']} {data['name']} {data['type']} {data['age']}岁 {data['info']} {data['notice']} {data['YL']} {data['MR']}",
                              font=("simsun", 14), wraplength=750)
        data_label.grid(row=n, column=0, sticky="w")

        # 创建一个删除按钮，点击后删除此项数据
        def delete_data(num):
            if messagebox.askyesno("确认删除", "确定要删除此项数据吗？"):
                data_dict.pop(num)
                data_label.destroy()
                delete_button.destroy()
                write_csv()  # 删除后保存数据到csv文件
        # 创建删除按钮
        delete_button = tk.Button(
            data_frame, text="删除", command=lambda number=num: delete_data(num), height=1, width=6)
        # delete_button.pack(side=tk.RIGHT)
        delete_button.grid(row=n, column=1, sticky="e", padx=(4, 4))
        n += 1

# 将数据保存到csv文件中
def write_csv():
    with open('pet111.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['编号number', '名name', '类型type',
                        '年龄age', '信息data', '注意notice', '医疗费用YL', '美容费用MR'])
        for num, data in data_dict.items():
            name = data['name']
            number = data['number']
            type = data['type']
            age = data['age']
            info = data['info']
            notice = data['notice']
            YL = data['YL']
            MR = data['MR']
            writer.writerow([number, name, type, age, info, notice, YL, MR])

def click1(button, i):
    button["text"] = "已选中"
    status_li[i-1] = 1
# 医美费用生成列表
def generate_dict():
    
    root1.geometry("550x550")

    dict_display_frame = tk.Frame(root1)
    dict_display_frame.grid()

    row_frame = tk.Frame(dict_display_frame)
    row_frame.grid(row=0, column=0, sticky="w")

    label = tk.Label(row_frame, text='项目', width=20)
    label.grid(row=0, column=0)

    label = tk.Label(row_frame, text='小型宠物', width=15)
    label.grid(row=0, column=1)

    label = tk.Label(row_frame, text='中型宠物', width=15)
    label.grid(row=0, column=2)

    label = tk.Label(row_frame, text='大型宠物', width=15)
    label.grid(row=0, column=3)

    row_frame = tk.Frame(dict_display_frame)
    row_frame.grid(row=1, column=0, sticky="w")

    label = tk.Label(row_frame, text='洗澡', width=20)
    label.grid(row=0, column=0)

    label = tk.Label(row_frame, text='30', width=10)
    label.grid(row=0, column=1)

    
    button1 = tk.Button(row_frame, text="未选中", command=lambda: click1(button1, 1))
    button1.grid(row=0, column=2)

    label = tk.Label(row_frame, text='50', width=10)
    label.grid(row=0, column=3)
    button2 = tk.Button(row_frame, text="未选中", command=lambda: click1(button2, 2))
    
    button2.grid(row=0, column=4)

    label = tk.Label(row_frame, text='70', width=10)
    label.grid(row=0, column=5)
    button3 = tk.Button(row_frame, text="未选中", command=lambda: click1(button3, 3))
    
    button3.grid(row=0, column=6)

    row_frame = tk.Frame(dict_display_frame)
    row_frame.grid(row=2, column=0, sticky="w")

    label = tk.Label(row_frame, text='理发', width=20)
    label.grid(row=0, column=0)

    label = tk.Label(row_frame, text='100', width=10)
    label.grid(row=0, column=1)
    button4 = tk.Button(row_frame, text="未选中", command=lambda: click1(button4, 4))
    
    button4.grid(row=0, column=2)

    label = tk.Label(row_frame, text='140', width=10)
    label.grid(row=0, column=3)
    button5 = tk.Button(row_frame, text="未选中", command=lambda: click1(button5, 5))
    
    button5.grid(row=0, column=4)

    label = tk.Label(row_frame, text='180', width=10)
    label.grid(row=0, column=5)
    button6 = tk.Button(row_frame, text="未选中", command=lambda: click1(button6, 6))
    
    button6.grid(row=0, column=6)
    # 添加“计算总价”按钮 
    cost_frame = tk.Frame(root1)
    cost_frame.grid()
    button = tk.Button(cost_frame, text="总价", command=lambda: calculate_total_price(status_li))
    button.pack(side="bottom")


# 计算总价
def calculate_total_price(li):
    beauty_cost = 0
    treatment_cost = 0
    selected = []
    print(status_li)
    if li[0]:
        beauty_cost += 30
        selected.append('洗澡')
    if li[1]:
        treatment_cost += 50
        selected.append('小型宠物')
    if li[2]:
        treatment_cost += 70
        selected.append('中型宠物')
    if li[3]:
        treatment_cost += 100
        selected.append('大型宠物')
    if li[4]:
        beauty_cost += 140
        selected.append('理发')
    if li[5]:
        treatment_cost += 180
        selected.append('小型宠物')
    print(beauty_cost + treatment_cost)
    total_price_label = tk.Label(root1, text="总价：{}元".format(beauty_cost + treatment_cost))
    total_price_label.grid(row=4, column=0)
    return beauty_cost, treatment_cost, selected

def rank_beauty_cost():
    sorted_data = sorted(data_dict.values(), key=lambda x: x["MR"], reverse=True)
    messagebox.showinfo("美容费用排名", "\n".join(["{}：{}元".format(data["name"], data["MR"]) for data in sorted_data]))

def rank_treatment_cost():
    sorted_data = sorted(data_dict.values(), key=lambda x: x["YL"], reverse=True)
    messagebox.showinfo("治疗费用排名", "\n".join(["{}：{}元".format(data["name"], data["YL"]) for data in sorted_data]))


# 主窗口
# 读取csv文件中的数据
read_csv()

# 创建宠物资料GUI窗口
root = tk.Tk()
root.title("添加宠物资料")
root.geometry("280x300")
root1 = tk.Tk()
root1.title("医美费用表")

# 创建输入框和标签
name_label = tk.Label(root, text="名字：")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

number_label = tk.Label(root, text="编号：")
number_label.grid(row=1, column=0)
number_entry = tk.Entry(root)
number_entry.grid(row=1, column=1)

type_label = tk.Label(root, text="类型：")
type_label.grid(row=2, column=0)
type_entry = tk.Entry(root)
type_entry.grid(row=2, column=1)

age_label = tk.Label(root, text="年龄：")
age_label.grid(row=3, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=3, column=1)

info_label = tk.Label(root, text="信息：")
info_label.grid(row=4, column=0)
info_entry = tk.Entry(root)
info_entry.grid(row=4, column=1)

YL_label = tk.Label(root, text="医疗费用：")
YL_label.grid(row=5, column=0)
YL_entry = tk.Entry(root)
YL_entry.grid(row=5, column=1)

MR_label = tk.Label(root, text="美容费用：")
MR_label.grid(row=6, column=0)
MR_entry = tk.Entry(root)
MR_entry.grid(row=6, column=1)

notice_label = tk.Label(root, text="注意：")
notice_label.grid(row=7, column=0)
notice_entry = tk.Entry(root)
notice_entry.grid(row=7, column=1)

# 创建提交按钮
submit_button = tk.Button(root, text="提交", command=submit)
submit_button.grid(row=8, column=1)

# 创建显示数据按钮
show_data_button = tk.Button(root, text="资料库", command=show_data)
show_data_button.grid(row=8, column=0)

# 添加查看“宠物医美费用”按钮
generate_dict_button = tk.Button(root, text="宠物医美费用", command=generate_dict)
generate_dict_button.grid(row=10, column=0)
dict_display_frame = tk.Frame(root1)
dict_display_frame.grid(row=0, column=0)

# 添加美容费用排名按钮
rank_beauty_cost_button = tk.Button(root, text="美容费用排名", command=rank_beauty_cost)
rank_beauty_cost_button.grid(row=9, column=0)

# 添加治疗费用排名按钮
rank_treatment_cost_button = tk.Button(root, text="治疗费用排名", command=rank_treatment_cost)
rank_treatment_cost_button.grid(row=9, column=1)
# 运行GUI窗口
root.mainloop()
root1.mainloop()
