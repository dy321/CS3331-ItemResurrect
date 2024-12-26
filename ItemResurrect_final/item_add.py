import tkinter as tk
import tkinter.messagebox as messagebox
import json
import os


class SuccessMessage:
    def __init__(self, master:tk.Tk):
        #页面布局
        self.root = master
        self.root.title('添加物品')
        self.root.geometry('300x130')

        self.page = tk.Frame(self.root)
        self.page.pack()
        tk.Label(self.page).grid(row=0, column=0)
        tk.Label(self.page, text='添加物品成功！').grid(row=1, column=1, pady=10)

        tk.Button(self.page, text='返回', command=self.back).grid(row=2, column=1)

    #返回上一级
    def back(self):
        from homepage import HomePage
        self.page.destroy()
        HomePage(self.root)



class AddPage:
    def __init__(self, master: tk.Tk, type_index: int, type_name:str):
        # 页面布局
        self.root = master
        self.root.title('ItemResurrect-add')
        self.root.geometry('600x400')

        # 变量说明
        self.name = tk.StringVar()
        self.contact = tk.StringVar()
        self.introduction = tk.StringVar()
        self.mail = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.p1 = tk.StringVar()
        self.p2 = tk.StringVar()
        self.p3 = tk.StringVar()

        self.page = tk.Frame(self.root)
        self.page.pack()

        # 变量输入
        tk.Label(self.page).grid(row=0, column=0)
        # 添加提示信息：您正在进行添加xx类物品
        tk.Label(self.page, text=f"您正在进行添加 {type_name} 的操作…", font=("Arial", 12)).grid(row=0, column=1, columnspan=4, pady=10)
        tk.Label(self.page, text='  *物品名称：').grid(row=1, column=1, pady=10)
        tk.Entry(self.page, textvariable=self.name).grid(row=1, column=2, pady=10, padx=5)
        tk.Label(self.page, text='  *联系人：').grid(row=1, column=3, pady=10)
        tk.Entry(self.page, textvariable=self.contact).grid(row=1, column=4, pady=10, padx=5)        
        tk.Label(self.page, text='  联系电话：').grid(row=2, column=1, pady=10)
        tk.Entry(self.page, textvariable=self.phone).grid(row=2, column=2, pady=10, padx=5)
        tk.Label(self.page, text='  物品地址：').grid(row=2, column=3, pady=10)
        tk.Entry(self.page, textvariable=self.mail).grid(row=2, column=4, pady=10, padx=5)
        tk.Label(self.page, text='  说明：').grid(row=3, column=1, pady=10)
        tk.Entry(self.page, textvariable=self.introduction).grid(row=3, column=2)
        tk.Label(self.page, text='  邮箱：').grid(row=3, column=3, pady=10)
        tk.Entry(self.page, textvariable=self.email).grid(row=3, column=2)
        
        self.show_type(type_index)
        tk.Button(self.page, text='添加', command=self.add).grid(row=5, column=2, pady=100)
        tk.Button(self.page, text='返回', command=self.back).grid(row=5, column=4, pady=50)

    # 打开对应json
    def read(self, type_index: int):
        # 使用 os.path.join 构建相对路径
        file_path = os.path.join('Item database', f'{type_index}.json')
        with open(file_path, mode='r', encoding='utf-8') as f:
            content = f.read()
        self.contents = json.loads(content)

    # 写入对应json
    def write(self, type_index: int, json_content):
        # 使用 os.path.join 构建相对路径
        file_path = os.path.join('Item database', f'{type_index}.json')
        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(obj=json_content, ensure_ascii=False, fp=f)

    # 添加物品操作
    def add(self):
        if self.name.get() and self.contact.get():
            json_content = []
            self.read(self.type_index)
            # 读入json中原有数据
            for c in self.contents:
                ob = {}
                ob['name'] = c['name']
                ob['contact'] = c['contact']
                ob['phone'] = c['phone']
                ob['mail'] = c['mail']
                ob['introduction'] = c['introduction']
                ob['email'] = c['email']
                ob['p1'] = c['p1']
                ob['p2'] = c['p2']
                ob['p3'] = c['p3']
                json_content.append(ob)
            # 添加新数据
            object = {}
            object['name'] = self.name.get()
            object['contact'] = self.contact.get()
            object['phone'] = self.phone.get()
            object['mail'] = self.mail.get()
            object['introduction'] = self.introduction.get()
            object['email'] = self.email.get()
            object['p1'] = self.p1.get()
            object['p2'] = self.p2.get()
            object['p3'] = self.p3.get()
            json_content.append(object)
            self.write(self.type_index, json_content)
            self.page.destroy()
            SuccessMessage(self.root)
        else:
            messagebox.showwarning(title='提示', message='很抱歉，*标识为必填项')

    # 展示对应属性
    def show_type(self, type_index: int):
        with open('Item database/types.json', mode='r', encoding='utf-8') as f:
            text = f.read()
        self.types = json.loads(text)
        self.type_index = type_index

        # 动态生成属性输入框
        for i, p in enumerate(['p1', 'p2', 'p3']):
                if self.types[type_index - 1][p]:
                    if i == 0:  # p1 位于第三行右
                        tk.Label(self.page, text=self.types[type_index - 1][p] + ':').grid(row=3, column=3, pady=10)
                        tk.Entry(self.page, textvariable=getattr(self, p)).grid(row=3, column=4, padx=10)
                    elif i == 1:  # p2 位于第四行左
                        tk.Label(self.page, text=self.types[type_index - 1][p] + ':').grid(row=4, column=1, pady=10)
                        tk.Entry(self.page, textvariable=getattr(self, p)).grid(row=4, column=2, padx=10)
                    elif i == 2:  # p3 位于第四行右
                        tk.Label(self.page, text=self.types[type_index - 1][p] + ':').grid(row=4, column=3, pady=10)
                        tk.Entry(self.page, textvariable=getattr(self, p)).grid(row=4, column=4, padx=10)

    # 返回上一层
    def back(self):
        from homepage import ChooseTypePage
        self.page.destroy()
        ChooseTypePage(self.root, 'add')

