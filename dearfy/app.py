from dearfy.base import Item, DOMNode

# ! App Base Class

class App(DOMNode[Item]):
    def __init__(self, **kwargs: object) -> None:
        super().__init__()
        self.kwargs = kwargs
        self.__dearfy_compose__()
        self._nodes.clear()

    def __dearfy_compose__(self) -> None:
        self._nodes.append(self)
        for child in self.compose():
            if self._current_node:
                self._current_node._add_child(child)
        self._nodes.clear()