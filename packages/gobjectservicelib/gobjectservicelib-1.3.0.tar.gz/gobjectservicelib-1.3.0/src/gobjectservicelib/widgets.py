"""Widget baseclasses"""
from typing import Any

import gi  # type: ignore

gi.require_version("Gtk", "3.0")
# pylint: disable=C0413
from gi.repository import Gtk  # type: ignore

from .service import BaseService


class ServiceWidgetBase(Gtk.Box):  # type: ignore
    """basclass for widget that need to be calling things from the service instance"""

    def __init__(self, service: BaseService, *args: Any, **kwargs: Any) -> None:
        self._service = service
        self._aioloop = service._aioloop
        super().__init__(*args, **kwargs)


class ServiceWindowBase(Gtk.Window):  # type: ignore
    """basclass for a window that needs to be calling things from the service instance"""

    def __init__(self, service: BaseService, *args: Any, **kwargs: Any) -> None:
        self._service = service
        self._aioloop = service._aioloop
        super().__init__(*args, **kwargs)
