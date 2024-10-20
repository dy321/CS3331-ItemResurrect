import tkinter as tk
from tkinter import messagebox, scrolledtext
from ItemManager import ItemManager

class ItemResurrectApp:
    """GUI界面类,用于处理物品的交互和显示。"""
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活软件")
        self.root.geometry("600x450")
        
        self.manager = ItemManager()

        # 创建标签和输入框
        self.create_input_frame()

        # 创建文本框用于显示信息
        self.result_box = scrolledtext.ScrolledText(self.root, width=70, height=15, wrap=tk.WORD)
        self.result_box.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def create_input_frame(self):
        # 输入框
        tk.Label(self.root, text="物品名称:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="物品描述:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.description_entry = tk.Entry(self.root, width=50)
        self.description_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="联系人信息:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.contact_entry = tk.Entry(self.root, width=50)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=5)

        # 按钮
        tk.Button(self.root, text="添加物品", command=self.add_item).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self.root, text="删除物品", command=self.delete_item).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.root, text="查找物品", command=self.find_item).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.root, text="显示所有物品", command=self.show_items).grid(row=4, column=1, padx=10, pady=5)

    def add_item(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        contact = self.contact_entry.get()

        if not name or not description or not contact:
            messagebox.showwarning("输入错误", "请完整填写所有字段！")
            return

        result = self.manager.add_item(name, description, contact)
        self.show_result(result)
        self.clear_entries()

    def delete_item(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("输入错误", "请填写要删除的物品名称！")
            return

        result = self.manager.delete_item(name)
        self.show_result(result)
        self.clear_entries()

    def find_item(self):
        name = self.name_entry.get()
        description = self.description_entry.get()

        if not name:
            messagebox.showwarning("输入错误", "请至少填写物品名称！")
            return

        result = self.manager.find_item(name=name, description=description if description else None)
        self.show_result(result)

    def show_items(self):
        result = self.manager.show_items()
        self.show_result(result)

    def show_result(self, result):
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result)

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)