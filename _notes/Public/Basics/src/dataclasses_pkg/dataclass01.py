from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
    
    def pricey(self):
        print(f"{self.name} bought it for {self.total_cost()}")


# obj = InventoryItem("Abhiram",4,5)
# obj.pricey()


@dataclass
class Superhero:
    """
    A class of superheroes and properties about their appearance in Marvel movies
    """
    name: str
    superpower: str = "Killing"
    appearances: int = 0

    def beckon(self):
	    print(f"{self.name} with the super power - {self.superpower} has appeared in Marvel movies {self.appearances} times")

class Superhero_nodc():
    """
    A class of superheroes and properties about their appearance in Marvel movies
    """
    def __init__(self, name, superpower,appearances=0):
         
        self.name = name
        self.superpower = superpower
        self.appearances = appearances

    def beckon(self):
	    print(f"{self.name} with the super power - {self.superpower} has appeared in Marvel movies {self.appearances} times")
         


         

superhero = Superhero("Aquaman","Underwater breathing",2)
superhero.beckon()