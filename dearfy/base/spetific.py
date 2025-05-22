from __future__ import annotations

import dearpygui.dearpygui as dpg
# > Local Imports
from dearfy.base.item import Item
from dearfy.base.require_bases import RequireBasesMeta, require_bases

# ! Enableable Spetific Class

@require_bases(Item)
class Enableable(metaclass=RequireBasesMeta):
    @property
    def enabled(self) -> bool:
        return self._config['enabled']
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.configurate(enabled=value)

# ! Showable Spetific Class

@require_bases(Item)
class Showable(metaclass=RequireBasesMeta):
    def show(self) -> None:
        if self.inited and (not self._config['show']):
            dpg.show_item(self.tag)
            self._config['show'] = True
    
    def hide(self) -> None:
        if self.inited and self._config['show']:
            dpg.hide_item(self.tag)
            self._config['show'] = False