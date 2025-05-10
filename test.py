from dearfy.app import App
from dearfy.widgets import *
from rich.console import Console

# ! App

class MyApp(App):
    def compose(self):
        self.button = Button(label='*click*', callback='test')
        with Window(label='Title'):
            with Group(horizontal=True):
                yield Text('Click for SURPRISE: ')
                yield self.button
    
    def action_test(self, sender: str | int):
        self.button.destroy()

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