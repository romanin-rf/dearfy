from dearfy.app import App, action, ComposeResult
from dearfy.widgets import *
from dearfy.handlers import ClickedHandler
from rich.console import Console

# ! App

class MyApp(App):
    def compose(self) -> ComposeResult:
        with Window(label='Title'):
            with Group(horizontal=True):
                with Text('Click for SURPRISE: '):
                    yield ClickedHandler(callback='test')
                yield Button(label='*click*', callback='test')
    
    @action('test')
    def action_test(self: 'MyApp', sender: str | int):
        console.print(self.get_item(sender))

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