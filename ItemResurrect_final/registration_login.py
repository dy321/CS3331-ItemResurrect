import tkinter as tk
import tkinter.messagebox
from homepage import HomePage  # 导入主页面类
import json



class LoginPage:
    """登录界面"""

    def __init__(self, master):
        # 将画板绑定到实例对象
        self.root = master
        # self.page 画纸
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.root.geometry("%dx%d" % (300, 180))

        # tkinter 提供的可变变量
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # 网格布局
        # 设置列权重，使布局更加灵活
        self.page.columnconfigure(0, weight=1)
        self.page.columnconfigure(1, weight=1)
        # 空白行
        tk.Label(self.page).grid(row=0, column=0, columnspan=2)
        # 用户名输入框
        tk.Label(self.page, text="账户").grid(row=1, column=0, sticky=tk.E, pady=10)
        tk.Entry(self.page, textvariable=self.username).grid(row=1, column=1, columnspan=1, sticky=tk.W, pady=10)
        # 密码输入框
        tk.Label(self.page, text="密码").grid(row=2, column=0, sticky=tk.E, pady=10)
        password_entry = tk.Entry(self.page, textvariable=self.password, show="*")
        password_entry.grid(row=2, column=1, columnspan=1, sticky=tk.W, pady=10)
        password_entry.bind("<Return>", self.login_check_with_event)  # 绑定回车键事件
        # 登录按钮
        tk.Button(self.page, text="登录", command=self.login_check).grid(row=3, column=0, sticky=tk.E, pady=10, padx=10)
        # 注册按钮
        tk.Button(self.page, text="还没有账号？点我注册！", command=self.open_register_page).grid(row=3, column=1, sticky=tk.W, pady=10, padx=10)
        # 增加空白行，使布局更美观
        tk.Label(self.page).grid(row=4, column=0, columnspan=2)


    def login_check(self):
        """检验登录"""
        # 拿到账号与密码
        name = self.username.get()
        pwd = self.password.get()
        
        try:
            with open("users.json", "r", encoding="utf-8") as fin:
                user = json.load(fin)
        except FileNotFoundError:
            tkinter.messagebox.showinfo(title='错误', message='用户文件丢失')
            return

        # 检查用户名是否存在
        user_exists = False
        for user_info in user:
            if user_info[0] == name:
                user_exists = True
                if user_info[1] == pwd:
                    print('恭喜登录成功')
                    # 摧毁当前页面绘制的内容
                    self.page.destroy()
                    # 页面的切换
                    HomePage(self.root)
                    return
                else:
                    tkinter.messagebox.showinfo(title='错误', message='密码错误')
                    return
                
        # 如果用户名不存在
        if not user_exists:
            tkinter.messagebox.showinfo(title='错误', message='用户名不存在，请注册')
    

    def login_check_with_event(self, event):
        """用于绑定回车键的登录方法"""
        self.login_check()

    def open_register_page(self):
        """打开注册页面"""
        self.page.destroy()  # 关闭当前登录页面
        RegisterPage(self.root)  # 打开注册页面



class RegisterPage:
    """注册界面"""
    def __init__(self, master):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.root.title('注册')
        self.root.geometry('230x220')

        # 用户注册标题
        tk.Label(self.page, text='用户注册').grid(row=0, column=0, columnspan=2)
        # 用户名
        tk.Label(self.page, text='用户名：').grid(row=1, column=0, sticky=tk.E)
        self.names = tk.Entry(self.page)
        self.names.grid(row=1, column=1)
        # 密码
        tk.Label(self.page, text='密码：').grid(row=2, column=0, sticky=tk.E)
        self.passwds = tk.Entry(self.page, show='*')
        self.passwds.grid(row=2, column=1)
        # 确认密码
        tk.Label(self.page, text='确认密码：').grid(row=3, column=0, sticky=tk.E)
        self.repasswd = tk.Entry(self.page, show='*')
        self.repasswd.grid(row=3, column=1)
        # 手机号
        tk.Label(self.page, text='手机号：').grid(row=4, column=0, sticky=tk.E)
        self.phonenum = tk.Entry(self.page)
        self.phonenum.grid(row=4, column=1)
        # 地址
        tk.Label(self.page, text='地址：').grid(row=5, column=0, sticky=tk.E)
        self.address = tk.Entry(self.page)
        self.address.grid(row=5, column=1)
        # 注册按钮
        tk.Button(self.page, text='注册', command=self.register).grid(row=6, column=0, sticky=tk.E, padx=5, pady=10)
        # 返回登录页面按钮
        tk.Button(self.page, text='已有账号？请返回', command=self.back_to_login).grid(row=6, column=1, sticky=tk.W, padx=5, pady=10)


    def register(self):
        """注册逻辑"""
        # 获取输入内容
        username = self.names.get()
        password = self.passwds.get()
        confirm_password = self.repasswd.get()
        phone = self.phonenum.get()
        address = self.address.get()

        # 检查用户名是否已存在
        try:
            with open("users.json", "r", encoding="utf-8") as fin:
                users = json.load(fin)
        except FileNotFoundError:
            users = []
        # 检查用户名是否重复
        if any([user[0] == username for user in users]):
            tkinter.messagebox.showerror(title='错误', message='用户名已存在')
            return
        # 检查密码长度
        if len(password) < 6:
            tkinter.messagebox.showerror(title='错误', message='密码不应少于6位')
            return
        # 检查两次密码是否一致
        if password != confirm_password:
            tkinter.messagebox.showerror(title='错误', message='两次密码不相同')
            return
        # 检查手机号格式
        if not (phone.isdigit() and len(phone) == 11):
            tkinter.messagebox.showerror(title='错误', message='请输入正确的11位手机号')
            return
        # 检查地址是否为空
        if not address:
            tkinter.messagebox.showerror(title='错误', message='地址不能为空')
            return

        # 注册成功，保存用户信息
        users.append([username, password, phone, address])
        with open("users.json", "w", encoding="utf-8") as fout:
            json.dump(users, fout, ensure_ascii=False, indent=4)

        tkinter.messagebox.showinfo(title='成功', message='注册成功！欢迎您:)')
        self.page.destroy()  # 关闭注册页面
        LoginPage(self.root)  # 返回登录页面


    def back_to_login(self):
        """返回登录页面"""
        self.page.destroy()  # 关闭当前注册页面
        LoginPage(self.root)  # 重新打开登录页面
