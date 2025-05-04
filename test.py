import sys
from dearfy.app import App
from dearfy.base import Item, Container
from rich.console import Console

# ! Types

class MyApp(App):
    def compose(self):
        yield Item()
        yield Item()
        with Container():
            yield Item()
            with Container():
                yield Item()
        yield Item()

# ! Variables

console = Console()

# ! Main

def main(*argv: str) -> int:
    console.print(MyApp()._to_rich_tree())
    return 0

# ! Start

if __name__ == '__main__':
    exit(main(*sys.argv))