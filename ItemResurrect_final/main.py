"""
“物品复活”软件: ItemResurrect
该程序允许添加物品的信息（物品名称，物品描述，联系人信息），删除物品的信息，显示物品列表，查找物品的信息
"""

import tkinter as tk
from registration_login import *  # 从模块中导入类



if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
