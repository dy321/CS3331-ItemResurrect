import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from fuzzywuzzy import fuzz


# 所有搜索物品操作的父类
class FindPage:
    def __init__(self, master: tk.Tk, type_index: int, type_name: str):
        # 页面布局
        self.root = master
        self.root.title('ItemResurrect-find')
        self.root.geometry('800x500')

        # 保存类型索引和名称
        self.type_index = type_index
        self.type_name = type_name

        # 创建页面
        self.create_page()

        # 变量说明、变量输入
        self.s_name = tk.StringVar()

        # 创建一个 Frame 用于容纳搜索框和提示信息
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(fill=tk.X, padx=20, pady=20)

        # 搜索框和标签
        self.label = tk.Label(self.search_frame, text='物品名称：')
        self.label.pack(side=tk.LEFT, padx=(0, 10))  # 靠左对齐，右侧留出间距
        self.entry = tk.Entry(self.search_frame, textvariable=self.s_name, width=30)
        self.entry.pack(side=tk.LEFT, fill=tk.X)  
        # 提示信息
        self.label_hint = tk.Label(self.search_frame, text=f"您正在进行查找 {self.type_name} 的操作…", font=("Arial", 12))
        self.label_hint.pack(padx=40)  
        # 搜索按钮
        self.bt1 = tk.Button(self.root, text='搜索', command=self.show_data_frame)
        self.bt1.pack(anchor=tk.W, padx=130, pady=20)
        # 返回按钮
        self.bt2 = tk.Button(self.root, text='返回', command=self.back)
        self.bt2.pack(anchor=tk.E, padx=20, pady=20)

        # 在页面初始化时展示所有物品信息
        self.show_data_frame()

    # 使用 Treeview 搭建展示数据的框架
    def create_page(self):
        # 创建一个 Frame 用于容纳 Treeview 和滚动条
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))  # 顶部留出间距

        # 创建 Treeview 和滚动条
        with open('Item database/types.json', mode='r', encoding='utf-8') as f:
            self.types = json.load(f)

        # 定义列名
        columns = ['name', 'contact', 'phone', 'mail', 'introduction', 'email', 'p1', 'p2', 'p3']
        self.tree_view = ttk.Treeview(self.content_frame, show='headings', columns=columns)

        # 设置列宽和居中对齐
        self.tree_view.column('name', width=80, anchor='center')
        self.tree_view.column('contact', width=80, anchor='center')
        self.tree_view.column('phone', width=100, anchor='center')
        self.tree_view.column('mail', width=100, anchor='center')
        self.tree_view.column('introduction', width=120, anchor='center')
        self.tree_view.column('email', width=100, anchor='center')
        self.tree_view.column('p1', width=80, anchor='center')
        self.tree_view.column('p2', width=80, anchor='center')
        self.tree_view.column('p3', width=80, anchor='center')

        # 添加竖向滚动条
        self.roll_vertical = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
        self.roll_vertical.pack(side='right', fill='y')
        self.tree_view.configure(yscrollcommand=self.roll_vertical.set)

        # 添加横向滚动条
        self.roll_horizontal = ttk.Scrollbar(self.content_frame, orient=tk.HORIZONTAL, command=self.tree_view.xview)
        self.roll_horizontal.pack(side='bottom', fill='x')
        self.tree_view.configure(xscrollcommand=self.roll_horizontal.set)

        # 显示表头
        self.tree_view.heading('name', text='名称')
        self.tree_view.heading('contact', text='联系人')
        self.tree_view.heading('phone', text='手机')
        self.tree_view.heading('mail', text='地址')
        self.tree_view.heading('introduction', text='说明')
        self.tree_view.heading('email', text='邮箱')
        self.headings()

        self.tree_view.pack(fill=tk.BOTH, expand=True)

    # 返回上一层
    def back(self):
        from homepage import ChooseTypePage
        self.tree_view.destroy()
        self.bt1.destroy()
        self.bt2.destroy()
        self.label.destroy()
        self.entry.destroy()
        self.roll_vertical.destroy()
        self.roll_horizontal.destroy()
        self.search_frame.destroy()
        self.content_frame.destroy()
        ChooseTypePage(self.root, action='find')

    # 展示具体数据
    def show_data_frame(self):
        # 清空 Treeview
        for child in self.tree_view.get_children():
            self.tree_view.delete(child)

        # 获取用户输入的物品名称
        thename = self.s_name.get()
        self.flag = 0  # 物品存在的标志

        # 读取数据
        self.read()

        # 搜索物品
        for item in self.items:
            if not thename:  # 如果未输入名称，展示所有物品
                self.tree_view.insert('', tk.END, values=(
                    item['name'], item['contact'], item['phone'], item['mail'], item['introduction'], item['email'],
                    item['p1'], item['p2'], item['p3']
                ))
                self.flag = 1
            else:
                # 使用模糊匹配比较名称
                match_ratio = fuzz.ratio(thename.lower(), item['name'].lower())
                if match_ratio > 50:  # 设置阈值
                    self.tree_view.insert('', tk.END, values=(
                        item['name'], item['contact'], item['phone'], item['mail'], item['introduction'], item['email'],
                        item['p1'], item['p2'], item['p3']
                    ))
                    self.flag = 1

        # 如果物品不存在，提示用户
        if self.flag == 0 and thename:
            messagebox.showwarning(title='提示', message='很抱歉，该物品不存在')

    # 读入不同类型物品的特有属性（父类中空实现）
    def headings(self):
        self.tree_view.heading('p1', text=self.types[self.type_index - 1]['p1'])
        self.tree_view.heading('p2', text=self.types[self.type_index - 1]['p2'])
        self.tree_view.heading('p3', text=self.types[self.type_index - 1]['p3'])

    # 打开对应的 JSON（父类中空实现）
    def read(self):
        file_path = os.path.join('Item database', f'{self.type_index}.json')
        with open(file_path, mode='r', encoding='utf-8') as f:
            self.items = json.load(f)
