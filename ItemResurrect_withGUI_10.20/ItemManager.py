from Item import Item

class ItemManager:
    """物品管理类，用于处理物品的添加、删除、查找等操作。"""
    def __init__(self):
        self.items = []

    def add_item(self, name, description, contact):
        """添加新物品到列表中，不要求物品名称唯一。"""
        new_item = Item(name, description, contact)
        self.items.append(new_item)
        return f"物品 '{name}' 添加成功！"

    def delete_item(self, name):
        """删除指定名称的物品（删除所有该名称的物品）。"""
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.name != name]
        deleted_count = initial_length - len(self.items)

        if deleted_count > 0:
            return f"已删除 {deleted_count} 个名称为 '{name}' 的物品！"
        else:
            return f"未找到名称为 '{name}' 的物品！"

    def show_items(self):
        """显示当前列表中的所有物品。"""
        if not self.items:
            return "没有物品可显示。"
        return "\n".join([str(item) for item in self.items])

    def find_item(self, name=None, description=None):
        """按名称和描述查询物品，名称需要完全匹配，描述模糊匹配。"""
        if not name:
            return "请至少输入物品名称。"
        
        # 如果只输入了物品名称，返回所有名称匹配的物品
        if description is None:
            found_items = [item for item in self.items if item.name == name]
            if not found_items:
                return f"未找到名称为 '{name}' 的物品。"
            return "\n".join([str(item) for item in found_items])
        
        # 如果同时输入了名称和描述，名称完全匹配，描述模糊匹配
        found_items = [
            item for item in self.items 
            if item.name == name and description.lower() in item.description.lower()
        ]
        if not found_items:
            return f"未找到名称为 '{name}' 且描述包含 '{description}' 的物品。"
        return "\n".join([str(item) for item in found_items])