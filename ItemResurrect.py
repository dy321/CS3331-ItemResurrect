"""

“物品复活“软件: ItemResurrect

该程序允许添加物品的信息（物品名称，物品描述，联系人信息），删除物品的信息，显示物品列表，也允许查找物品的信息

"""

class Item:
    """物品类，用于存储物品信息。"""
    def __init__(self, name, description, contact):
        self.name = name
        self.description = description
        self.contact = contact

    def __str__(self):
        return f"名称: {self.name}, 描述: {self.description}, 联系人: {self.contact}"


class ItemManager:
    """物品管理类，用于处理物品的添加、删除、查找等操作。"""
    def __init__(self):
        self.items = {}

    def add_item(self, name, description, contact):
        """添加新物品到列表中，确保物品名称唯一。"""
        if name in self.items:
            return f"物品 '{name}' 已存在，无法添加！"
        
        new_item = Item(name, description, contact)
        self.items[name] = new_item
        return f"物品 '{name}' 添加成功！"

    def delete_item(self, name):
        """从列表中删除指定名称的物品。"""
        if name in self.items:
            del self.items[name]
            return f"物品 '{name}' 已删除！"
        return f"未找到物品 '{name}'！"

    def show_items(self):
        """显示当前列表中的所有物品。"""
        if not self.items:
            return "没有物品可显示。"
        return "\n".join([str(item) for item in self.items.values()])

    def find_item(self, substring):
        """查找指定名称的物品。"""
        found_items = [item for item in self.items.values() if substring.lower() in item.name.lower()]
        if not found_items:
            return f"未找到包含 '{substring}' 的物品！"
        return "\n".join([str(item) for item in found_items])


def main():
    manager = ItemManager()

    while True:
        print("\n物品复活软件")
        print("1. 添加物品")
        print("2. 删除物品")
        print("3. 显示所有物品")
        print("4. 查找物品")
        print("5. 退出")
        choice = input("请选择一个操作: ")

        try:
            if choice == '1':
                name = input("请输入物品名称: ")
                description = input("请输入物品描述: ")
                contact = input("请输入联系人信息: ")
                print(manager.add_item(name, description, contact))
            
            elif choice == '2':
                name = input("请输入要删除的物品名称: ")
                print(manager.delete_item(name))
            
            elif choice == '3':
                print(manager.show_items())
            
            elif choice == '4':
                substring = input("请输入要查找的物品名称的子字符串: ")
                print(manager.find_item(substring))
            
            elif choice == '5':
                print("退出程序。")
                break
            
            else:
                print("无效选择，请重试。")

        except Exception as e:
            print(f"程序发生错误: {e}")


if __name__ == "__main__":
    main()
