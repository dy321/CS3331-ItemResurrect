class Item:
    """物品类，用于存储物品信息。"""
    def __init__(self, name, description, contact):
        self.name = name
        self.description = description
        self.contact = contact

    def __str__(self):
        return f"名称: {self.name}, 描述: {self.description}, 联系人: {self.contact}"