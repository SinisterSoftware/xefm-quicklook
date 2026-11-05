"""QuickLook 連携 (~/.xefm/extensions/quicklook.py)

Z: カーソル位置のファイルを QuickLook で開く。未起動なら起動する。
アクティブペインが左なら画面右端、右なら左端に、XeFM と同じモニタで表示する。
"""
import subprocess
import time

import psutil
import win32api
import win32con
import win32gui
import win32process

WIDTH, HEIGHT = 600, 800
PROC_NAME = "quicklook.exe"
STARTUP_WAIT = 1.5      # 初回起動を待つ秒数
OPEN_WAIT = 1.0         # ウィンドウが出るのを待つ秒数


def _running():
    return any((p.info["name"] or "").lower() == PROC_NAME
               for p in psutil.process_iter(["name"]))


def _windows():
    """QuickLook の可視トップレベルウィンドウ (タイトルありのもの)。"""
    pids = {p.pid for p in psutil.process_iter(["name"])
            if (p.info["name"] or "").lower() == PROC_NAME}
    found = []

    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            if win32process.GetWindowThreadProcessId(hwnd)[1] in pids:
                found.append(hwnd)
        return True

    win32gui.EnumWindows(cb, None)
    return found


def _place(hwnd, xefm_hwnd, left_pane_active):
    mon = win32api.MonitorFromWindow(xefm_hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    wl, wt, wr, wb = win32api.GetMonitorInfo(mon)["Work"]    # タスクバーを除いた範囲
    height = min(HEIGHT, wb - wt)
    x = wr - WIDTH if left_pane_active else wl
    win32gui.SetWindowPos(hwnd, 0, x, wt, WIDTH, height, win32con.SWP_NOZORDER)


def quicklook(ctx):
    entry = ctx.pane.focused
    if entry is None:
        return
    path = str(entry.path)
    if "://" in path:
        ctx.message("quicklook: 仮想フォルダ内のファイルは開けません")
        return

    # QuickLook 起動でフォーカスが移る前に、XeFM のウィンドウとペイン位置を控える
    xefm_hwnd = win32gui.GetForegroundWindow()
    left_active = ctx.pane.name == "left"

    if not _running():
        subprocess.Popen([PROC_NAME])
        time.sleep(STARTUP_WAIT)
    subprocess.Popen(["quicklook", path])
    time.sleep(OPEN_WAIT)

    hwnds = _windows()
    if hwnds:
        _place(hwnds[0], xefm_hwnd, left_active)


ACTIONS = {"quicklook": {"func": quicklook, "description": "Preview the cursor file with QuickLook"}}
KEY_BINDINGS = {"quicklook": ["Alt-Z"]}

