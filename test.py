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
                with Text('Click for SURPRISE: ', tag='text-click-surprise'):
                    with Tooltip(delay=0.2):
                        yield Text(':3')
                yield Button(label='*click*', callback='test', tag='click-button')
        yield ClickedItemHandler(callback='test', parent='text-click-surprise')
        with Tooltip(delay=0.2, parent='click-button'):
            yield Text(':3')
    
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