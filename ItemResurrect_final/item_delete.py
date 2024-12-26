import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from fuzzywuzzy import fuzz


# 所有删除物品操作的父类
class DeletePage:
    def __init__(self, master: tk.Tk, type_index: int, type_name: str):
        # 页面布局
        self.root = master
        self.root.title('ItemResurrect-delete')
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
        self.entry.bind("<KeyRelease>", self.search_data)  # 绑定搜索事件
        # 提示信息
        self.label_hint = tk.Label(self.search_frame, text=f"您正在进行删除 {self.type_name} 的操作…", font=("Arial", 12))
        self.label_hint.pack(padx=40)  
        # 删除按钮
        self.delete_button = tk.Button(self.root, text='删除', command=self.delete_data_frame)
        self.delete_button.pack(anchor=tk.W, padx=220, pady=20)
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
        self.delete_button.destroy()
        self.bt2.destroy()
        self.label.destroy()
        self.entry.destroy()
        self.roll_vertical.destroy()
        self.roll_horizontal.destroy()
        self.search_frame.destroy()
        self.content_frame.destroy()
        ChooseTypePage(self.root, action='delete')

    # 删除具体数据
    def delete_data_frame(self):
        # 获取用户选择的物品
        selected_item = self.tree_view.selection()
        if not selected_item:
            messagebox.showwarning(title='提示', message='请选择一个物品')
            return

        # 获取选中行的物品名称
        item_name = self.tree_view.item(selected_item, 'values')[0]
        
        # 弹出确认对话框
        confirm = messagebox.askyesno(title='确认删除', message=f'您确定要删除物品 "{item_name}" 吗？')
        if not confirm:
            return

        # 读取数据
        self.read()

        # 删除物品
        updated_items = []
        self.flag = 0  # 物品存在的标志
        for item in self.items:
            if item_name == item['name']:  # 如果输入名称匹配，跳过该物品
                self.flag = 1
                continue
            updated_items.append(item)

        # 如果物品存在，写入更新后的数据
        if self.flag:
            self.write(updated_items)
            messagebox.showinfo(title='提示', message='物品删除成功！')
            self.show_data_frame()  # 刷新显示
        else:
            messagebox.showwarning(title='提示', message='很抱歉，该物品不存在')

    # 展示具体数据
    def show_data_frame(self):
        # 清空 Treeview
        for child in self.tree_view.get_children():
            self.tree_view.delete(child)

        # 读取数据
        self.read()

        # 展示所有物品
        for item in self.items:
            self.tree_view.insert('', tk.END, values=(
                item['name'], item['contact'], item['phone'], item['mail'], item['introduction'], item['email'],
                item['p1'], item['p2'], item['p3']
            ))

    # 搜索物品
    def search_data(self, event=None):
        search_term = self.s_name.get().lower()

        # 清空 Treeview
        for child in self.tree_view.get_children():
            self.tree_view.delete(child)

        # 读取数据
        self.read()

        # 如果搜索框为空，则展示所有物品
        if not search_term:
            self.show_data_frame()
            return

        # 搜索并展示匹配的物品
        for item in self.items:
            # 使用模糊匹配查找名称
            if fuzz.partial_ratio(search_term, item['name'].lower()) > 50:  # 模糊匹配阈值
                self.tree_view.insert('', tk.END, values=(
                    item['name'], item['contact'], item['phone'], item['mail'], item['introduction'], item['email'],
                    item['p1'], item['p2'], item['p3']
                ))

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

    # 写入对应的 JSON（父类中空实现）
    def write(self, json_content):
        file_path = os.path.join('Item database', f'{self.type_index}.json')
        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(json_content, f, ensure_ascii=False, indent=4)
