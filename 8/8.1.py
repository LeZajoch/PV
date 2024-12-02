class IkeaItem:
    def __init__(self, shelf, row, name, price):
        self.shelf = shelf
        self.row = row
        self.name = name
        self.price = price

    def __repr__(self):
        return f"IkeaItem(shelf={self.shelf}, row='{self.row}', name='{self.name}', price={self.price})"

class MeasureableIkeaItem:
    def __init__(self, height, width, depth):
        self.height = height
        self.width = width
        self.depth = depth

    def __repr__(self):
        return f"MeasureableIkeaItem(height={self.height}, width={self.width}, depth={self.depth})"

class PlasticWasteIkeaItem:
    def __init__(self, plastic_weight):
        self.plastic_weight = plastic_weight

    def __repr__(self):
        return f"PlasticWasteIkeaItem(plastic_weight={self.plastic_weight})"

class LACK(IkeaItem, MeasureableIkeaItem):
    def __init__(self, shelf, row, name, price, height, width, depth, color):
        IkeaItem.__init__(self, shelf, row, name, price)
        MeasureableIkeaItem.__init__(self, height, width, depth)
        self.color = color

    def __repr__(self):
        return (f"LACK(shelf={self.shelf}, row='{self.row}', name='{self.name}', price={self.price}, "
                f"height={self.height}, width={self.width}, depth={self.depth}, color='{self.color}')")

class SAMLA_BOX(IkeaItem, MeasureableIkeaItem):
    def __init__(self, shelf, row, name, price, height, width, depth, volume):
        IkeaItem.__init__(self, shelf, row, name, price)
        MeasureableIkeaItem.__init__(self, height, width, depth)
        self.volume = volume

    def __repr__(self):
        return (f"SAMLA_BOX(shelf={self.shelf}, row='{self.row}', name='{self.name}', price={self.price}, "
                f"height={self.height}, width={self.width}, depth={self.depth}, volume={self.volume})")

class SJÖRAPPORT(IkeaItem):
    def __init__(self, shelf, row, name, price, expiration, weight):
        super().__init__(shelf, row, name, price)
        self.expiration = expiration
        self.weight = weight

    def __repr__(self):
        return (f"SJÖRAPPORT(shelf={self.shelf}, row='{self.row}', name='{self.name}', price={self.price}, "
                f"expiration='{self.expiration}', weight={self.weight})")




#USAGE

l1 = LACK(1, "A", "LACK", 100, 20, 30, 10, "blue")
print(l1)
s1 = SJÖRAPPORT(2, "B", "SJÖRAPPORT", 50, "2025-01-01", 1.2)
print(s1)
b1 = SAMLA_BOX(3, "C", "SAMLA_BOX", 20, 40, 50, 30, 60)
print(b1)
