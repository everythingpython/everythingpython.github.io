class InventoryItem_NoClass:
    """Class for keeping track of an item in inventory."""
    def __init__(self, name : str, unit_price: float, quantity_on_hand=0):    
        self.name = name
        self.unit_price = unit_price
        self.quantity_on_hand = quantity_on_hand

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
    
    def pricey(self):
        print(f"{self.name} bought it for {self.total_cost()}")


obj = InventoryItem_NoClass("Abhiram",4,5)
obj.pricey()
