"""Eventloop helpers"""
from typing import Optional, Any, Callable
import functools
import logging

from gi.repository import GLib as glib  # type: ignore

MAINLOOP_SINGLETON: Optional[glib.MainLoop] = None
LOGGER = logging.getLogger(__name__)


def singleton() -> glib.MainLoop:
    """Return singleton instance of the current loop"""
    global MAINLOOP_SINGLETON  # pylint: disable=W0603
    if not MAINLOOP_SINGLETON:
        MAINLOOP_SINGLETON = glib.MainLoop()
        # Monkeypatch the call_soon helper on the mainloop object
        MAINLOOP_SINGLETON.call_soon = call_soon
    return MAINLOOP_SINGLETON


def call_soon(glib_callback: Callable[..., Any], *args: Any) -> int:
    """Add a high-priority callback to the eventloop"""
    instance = singleton()
    if not instance.is_running():
        LOGGER.warning("Loop is not running yet, callback will be run when loop is started")
    return int(glib.timeout_add(0, glib_callback, *args, priority=glib.PRIORITY_HIGH))


def aio(func: Callable[..., Any]) -> Callable[..., Any]:
    """decorator to call the wrapped function in the aio main thread

    func MUST be a bound method in an instance that has self._aioloop"""

    @functools.wraps(func)
    def wrapped(self: Any, *args: Any) -> None:
        """wraps aioloop.call_soon_threadsafe"""
        self._aioloop.call_soon_threadsafe(func, self, *args)  # pylint: disable=W0212

    return wrapped


def gloop(func: Callable[..., Any]) -> Callable[..., Any]:
    """decorator to call the wrapped function in the glib mainloop thread"""

    @functools.wraps(func)
    def wrapped(self: Any, *args: Any) -> None:
        """wraps glib.timeout_add via the call_soon -helper"""
        call_soon(func, self, *args)

    return wrapped
