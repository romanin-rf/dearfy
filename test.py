from dearfy.app import App
from dearfy.widgets import *
from rich.console import Console

# ! App

class MyApp(App):
    def compose(self):
        with Window(label='Title'):
            with Group(horizontal=True):
                yield Text('Click for SURPRISE: ')
                yield Button(label='*click*')

# ! Variables

console = Console()

# ! Main

def main():
    app = MyApp()
    app.run()

# ! Start

if __name__ == '__main__':
    try:
        main()
    except:
        console.print_exception(width=console.width, show_locals=True)