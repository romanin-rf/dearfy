# dearfy

## Desription
A library to simplify the creation of complex applications using DearPyGUI (based on DearImGUI).

## Using

```python
from dearfy.app import App, action
from dearfy.widgets import *
from dearfy.handlers import ClickedHandler
from dearfy.typing import Tag


class MyApp(App):
    def compose(self) -> ComposeResult:
        with Window(label='Title'):
            with Group(horizontal=True):
                with Text('Click for SURPRISE: '):
                    yield ClickedHandler(callback='test0')
                yield Button(label='*click*', callback='test1')
    
    # Attribute handling is used, 
    # i.e. all functions that start with `action_` will be wrapped in `Action`.
    def action_test0(self, sender: Tag):
        print('!!! SURPRISE #1 !!!')
    
    # And it is possible not to write them through self, 
    # although if you decide to do it, 
    # you will have to wrap them in the action decorator anyway.
    @action('test1')
    def action_test1(self):
        print('!!! SURPRISE #2 !!!')
```

## Installing

So far, the project is still under development. So I don't recommend to use it as a basis for any project.