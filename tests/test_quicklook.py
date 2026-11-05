from types import SimpleNamespace

from quicklook.logic import quicklook

def test_no_focused_entry_is_a_noop():
    quicklook(SimpleNamespace(pane=SimpleNamespace(focused=None)))
