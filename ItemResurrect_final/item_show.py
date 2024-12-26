import tkinter as tk
from tkinter import ttk
import json
import os


class ShowPage:
    def __init__(self, master: tk.Tk, type_index: int, type_name: str):
        # 页面布局
        self.root = master
        self.root.title('ItemResurrect-show')
        self.root.geometry('800x500')

        # 保存类型索引和名称
        self.type_index = type_index
        self.type_name = type_name

        # 创建页面
        self.create_page()

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

        self.show_data_frame()

        # 创建一个 Frame 用于容纳提示信息和返回按钮
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)  # 底部留出间距

        # 添加提示信息：您正在进行展示 xx 类物品
        self.label = tk.Label(self.footer_frame, text=f"您正在进行展示 {self.type_name} 的操作…", font=("Arial", 12))
        self.label.pack(side=tk.LEFT, padx=(0, 20))  # 提示信息靠左，右侧留出间距

        # 返回按钮
        self.bt = tk.Button(self.footer_frame, text='返回', command=self.back)
        self.bt.pack(side=tk.RIGHT)  # 返回按钮靠右

    # 返回上一级
    def back(self):
        from homepage import ChooseTypePage
        self.tree_view.destroy()
        self.bt.destroy()
        self.label.destroy()
        self.footer_frame.destroy()
        self.content_frame.destroy()
        ChooseTypePage(self.root, action='show')

    # 展示具体数据
    def show_data_frame(self):
        self.read()
        for item in self.items:
            self.tree_view.insert('', tk.END, values=(
                item['name'], item['contact'], item['phone'], item['mail'], item['introduction'], item['email'],
                item['p1'], item['p2'], item['p3']
            ))

    # 显示表头
    def headings(self):
        # 根据 type_index 动态设置表头
        self.tree_view.heading('p1', text=self.types[self.type_index - 1]['p1'])
        self.tree_view.heading('p2', text=self.types[self.type_index - 1]['p2'])
        self.tree_view.heading('p3', text=self.types[self.type_index - 1]['p3'])

    # 打开对应的 JSON
    def read(self):
        # 使用 os.path.join 构建文件路径
        file_path = os.path.join('Item database', f'{self.type_index}.json')
        with open(file_path, mode='r', encoding='utf-8') as f:
            self.items = json.load(f)