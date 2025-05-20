import time
from rich.console import Console
# > Dearfy
from dearfy.widgets import *
from dearfy.handlers import *
from dearfy.typing import Tag
from dearfy.app import App, action, ComposeResult

# ! App

class MyApp(App):
    def compose(self) -> ComposeResult:
        with Window(label='Title'):
            with Group(horizontal=True):
                yield Text('Click for SURPRISE: ', tag='text-click-surprise')
                yield Button(label='*click*', callback='test')
        yield ClickedItemHandler(callback='test', parent='text-click-surprise')
    
    @action('test', callmode='one', blockmode='all', threaded=True)
    def action_test(app: 'MyApp', sender: Tag):
        console.print(app.get_item(sender))
        time.sleep(10)

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