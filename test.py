from dearfy.app import App
from dearfy.widgets.text import Text
from dearfy.widgets.window import Window
from rich.console import Console

# ! Types

class MyApp(App):
    def compose(self):
        with Window(label='Title'):
            with Text('test'):
                pass

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