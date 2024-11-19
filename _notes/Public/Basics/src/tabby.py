
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Markdown, TabbedContent, TabPane
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
         

items = dir(Superhero)
items2 = dir(Superhero_nodc)
items3 = [i for i in items if i not in items2]
items_ = "\n".join([f"- {i}" for i in items])
items2_ = "\n".join([f"- {i}" for i in items2])

JESSICA = f"""
# Class with no data class annotation

{items2_}


Number of attributes - {len(items2)}
"""

PAUL = f"""
# Dataclass

{items_}

Number of attributes - {len(items)}
"""


class TabbedApp(App):
    """An example of tabbed content."""

    BINDINGS = [
        ("j", "show_tab('jessica')", "Attributes of normal Classes"),
        ("p", "show_tab('paul')", "Attributes of dataclasses"),
    ]

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        yield Footer()

        # Add the TabbedContent widget
        with TabbedContent(initial="jessica"):
            with TabPane("Attributes of normal Classes", id="jessica"):
                yield Markdown(JESSICA)

            with TabPane("Attributes of dataclasses", id="paul"):
                yield Markdown(PAUL)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab


if __name__ == "__main__":
    app = TabbedApp()
    app.run()
