"""
“物品复活”软件: ItemResurrect
该程序允许添加物品的信息（物品名称，物品描述，联系人信息），删除物品的信息，显示物品列表，也允许查找物品的信息
"""

import tkinter as tk
from ItemResurrectApp import ItemResurrectApp  # 从模块中导入类

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemResurrectApp(root)
    root.mainloop()

