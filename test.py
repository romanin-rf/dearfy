from dearfy.app import App, action
from dearfy.widgets import *
from rich.console import Console

# ! App

class MyApp(App):
    def compose(self):
        with Window(label='Title'):
            with Group(horizontal=True):
                yield Text('Click for SURPRISE: ')
                yield Button(label='*click*', callback=self.action_method_testing)
    
    @action('method_testing')
    def action_method_testing(sender: str | int):
        console.print(f'call -> action_method_testing({sender!r})')

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