from __future__ import annotations

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