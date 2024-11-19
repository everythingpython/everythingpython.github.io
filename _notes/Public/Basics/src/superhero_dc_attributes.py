from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ListItem, ListView
from dataclasses import dataclass

@dataclass
class Superhero:
    """
    A class of superheroes and properties about their appearance in Marvel movies
    """
    name: str
    superpower: str
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
         


         

class ListViewExample(App):
    CSS_PATH = "list_view.tcss"
    def compose(self) -> ComposeResult:
        items = dir(Superhero)
        items2 = dir(Superhero_nodc)
        for i in items:
            yield ListView(
                ListItem(Label(i)) 
        )
            yield Footer()
        for i in items2:
            yield ListView(
                ListItem(Label(i)) 
        )
            yield Footer()


if __name__ == "__main__":
    app = ListViewExample()
    app.run()


