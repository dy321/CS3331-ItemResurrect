'''
用户的主界面-包含功能：
1.添加物品
2.查找物品
3.查看物品
4.删除物品
5.退出登录
'''
import tkinter as tk
import json
from item_add import AddPage
from item_find import FindPage
from item_show import ShowPage
from item_delete import DeletePage


class HomePage:
    def __init__(self, master:tk.Tk):
        # 页面布局
        self.root = master
        self.root.title('ItemResurrect')
        self.root.geometry('300x260')
        self.page = tk.Frame(self.root)
        self.page.pack()
        tk.Label(self.page).grid(row=0, column=0)

        tk.Button(self.page, text='添加物品', command=self.choose_types_add).grid(row=1, column=1, pady=20,padx=30)
        tk.Button(self.page, text='查找物品', command=self.choose_types_find).grid(row=1, column=2, pady=20,padx=30)
        tk.Button(self.page, text='查看物品', command=self.choose_types_show).grid(row=2, column=1, pady=20)
        tk.Button(self.page, text='删除物品', command=self.choose_types_delete).grid(row=2, column=2, pady=20)
        tk.Button(self.page, text='退出登录', command=self.back).grid(row=3, column=1, pady=20, columnspan=2)


    # 添加物品
    def choose_types_add(self):
        self.page.destroy()
        ChooseTypePage(self.root, action='add')
    # 查找物品
    def choose_types_find(self):
        self.page.destroy()
        ChooseTypePage(self.root, action='find')
    # 查看物品
    def choose_types_show(self):
        self.page.destroy()
        ChooseTypePage(self.root, action='show')
    # 删除物品
    def choose_types_delete(self):
        self.page.destroy()
        ChooseTypePage(self.root, action='delete')

    
    # 退出登录
    def back(self):
        self.page.destroy()
        from registration_login import LoginPage
        LoginPage(self.root)



class ChooseTypePage:
    def __init__(self, master: tk.Tk, action: str):
        self.root = master
        self.action = action  # 记录用户在主页面选择的功能
        self.root.title('选择物品类型')
        self.root.geometry('300x200')

        self.page = tk.Frame(self.root)
        self.page.pack()
        self.show_types()

    def show_types(self):
        with open('Item database/types.json', mode='r', encoding='utf-8') as f:
            types = json.load(f)

        # 添加标题
        tk.Label(self.page, text="选择物品类型", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=10)
        # 显示类别按钮
        for i, type_info in enumerate(types):
            tk.Button(self.page, text=type_info['type'], 
                      command=lambda t=type_info['type']: self.select_type(t)).grid(row=i // 2 + 1, column=i % 2, padx=10, pady=5)
        # 添加返回按钮
        tk.Button(self.page, text='返回', command=self.back).grid(row=len(types) // 2 + 2, column=0, columnspan=2, pady=10)

    def select_type(self, type_name):
        self.page.destroy()
        # 根据 type_name 查找对应的 type_index
        with open(r'Item database/types.json', mode='r', encoding='utf-8') as f:
            types = json.load(f)
        type_index = None
        for i, type_info in enumerate(types):
            if type_info['type'] == type_name:
                type_index = i + 1  # 索引从 1 开始
                break

        if self.action == 'add':
            AddPage(self.root, type_index, type_name)
        elif self.action == 'find':
            FindPage(self.root, type_index, type_name)
        elif self.action == 'show':
           ShowPage(self.root, type_index, type_name)
        elif self.action == 'delete':
            DeletePage(self.root, type_index, type_name)


    def back(self):
        self.page.destroy()
        HomePage(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()