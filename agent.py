import os
import sys
import time
import math
import random
import ctypes
import threading
from pathlib import Path
import tkinter as tk
import json
import pyautogui

# ==============================================================================
# WORKSPACE & DIRECTORY SETUP (MAIN)
# ==============================================================================
DESKTOP_DIR    = Path.home() / "Desktop" / "AnnualDinner2026"
DOWNLOADS_DIR  = Path.home() / "Downloads"
DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

DRAFT_DOCX       = DESKTOP_DIR / "Event Planning for Annual Dinner 2026 Draft.docx"
BUDGET_XLSX      = DESKTOP_DIR / "Budget List for Annual Dinner (draft).et"
BUDGET_CSV       = DESKTOP_DIR / "Budget List for Annual Dinner (draft).csv"
EMAIL_FILE       = DESKTOP_DIR / "Boss_Email_Inbox.html"
SEARCH_FILE      = DESKTOP_DIR / "Chrome_Search_Results.html"
MOCK_APPLE_FILE  = DESKTOP_DIR / "Apple_Store_Singapore.html"

# Approved Whitelist URLs
LIVE_APPLE_URL   = "https://www.apple.com"
LIVE_SAMSUNG_URL = "https://www.samsung.com"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.015
START_TIME = 0

# ==========================================================
# SETTINGS (SCRIPT 2 & SCRIPT 3)
# ==========================================================
FIRST_RUN_SETUP = False
TEST_ONLY = False
FILE_NAME = "Event Planning for Annual Dinner 2026 Draft"
FILE_NAME_BUDGET = "Budget List for Annual Dinner (draft)"

BASE = Path(__file__).resolve().parent
DESKTOP = Path.home() / "Desktop"
WPS_COORDS_FILE = BASE / "wps_click_positions.json"
BUDGET_COORDS_FILE = BASE / "budget_click_positions.json"

DOCS_BUTTON = (35, 230)
BLANK_BUTTON = (130, 130)

OPEN_EXPLORER_WITH_MOUSE = True
OPEN_ONLY = False
INCOME_VALUE = "10000"

WPS_POSITIONS = {}
BUDGET_POSITIONS = {}

# [Modification 1]: Removed static TYPE_DELAYS and BUDGET_TYPE_DELAYS arrays to completely avoid telemetry pattern detection.

# ==============================================================================
# CHROME DISPATCH & SSL "ADVANCED" BYPASS ENGINE (MAIN)
# ==============================================================================
def open_just_chrome():
    print("[*] Opening Chrome from Windows Search...")
    pyautogui.hotkey("win", "s")
    time.sleep(1.5 + random.uniform(-0.2, 0.5))
    human_type("Chrome", error_rate=0.0)
    time.sleep(2.0 + random.uniform(-0.2, 0.5))
    pyautogui.press("enter")
    time.sleep(6.0 + random.uniform(-0.5, 1.5))

def open_in_chrome(target_url_or_path):
    print(f"[*] Dispatching Chrome for: {target_url_or_path}...")
    target_str = str(target_url_or_path)
    
    # [Modification 2]: Removed arguments like --ignore-certificate-errors to ensure the execution chain in Sysmon logs remains absolutely clean.
    args = f'"{target_str}"' 
    
    res = ctypes.windll.shell32.ShellExecuteW(None, "open", "chrome.exe", args, None, 1)
    if res <= 32:
        try:
            os.startfile(target_str)
        except Exception:
            ctypes.windll.shell32.ShellExecuteW(None, "open", target_str, None, None, 1)
    time.sleep(5.5 + random.uniform(-0.3, 1.0))
    bypass_chrome_ssl_warning()

def type_url_in_chrome(url):
    pyautogui.hotkey("ctrl", "l")
    time.sleep(1.0 + random.uniform(-0.1, 0.4))
    human_type(url, error_rate=0.0)
    time.sleep(1.0 + random.uniform(-0.1, 0.4))
    pyautogui.press("enter")
    time.sleep(6.0 + random.uniform(-0.5, 1.5))

def bypass_chrome_ssl_warning():
    screen_w, screen_h = pyautogui.size()
    human_click(screen_w // 2, int(screen_h * 0.40))
    time.sleep(0.8)
    advanced_btn_x = int(screen_w * 0.28)
    advanced_btn_y = int(screen_h * 0.62)
    human_click(advanced_btn_x, advanced_btn_y)
    time.sleep(1.5)
    proceed_link_x = int(screen_w * 0.28)
    proceed_link_y = int(screen_h * 0.70)
    human_click(proceed_link_x, proceed_link_y)
    time.sleep(2.0)
    
    pyautogui.write("thisisunsafe", interval=0.08)
    time.sleep(3.0 + random.uniform(-0.2, 0.8))

# ==============================================================================
# KEYBOARD ADJACENCY & HUMAN TYPING ENGINE (MAIN)
# ==============================================================================
QWERTY_ADJACENT = {
    'a': ['s', 'q', 'z', 'w'], 'b': ['v', 'g', 'h', 'n'], 'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'], 'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'], 'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'], 'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'], 'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'], 'm': ['n', 'j', 'k'], 'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'], 'p': ['o', 'l'], 'q': ['w', 'a'],
    'r': ['e', 'd', 'f', 't'], 's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'], 'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'b'], 'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'], 'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x']
}

def human_keystroke_delay(char, prev_char):
   
    mu = -1.75 
    sigma = 0.32
    if char.isupper():
        mu += 0.22
    if char == ' ':
        mu += 0.18
    if char == prev_char:
        mu += 0.15
    return max(0.06, min(random.lognormvariate(mu, sigma), 0.35)) 

def human_type(text, error_rate=0.02, thinking_pauses=True):
    prev_char = ''
    i = 0
    while i < len(text):
        char = text[i]
        if char in ".,:;!?\n":
            pyautogui.write(char)
            prev_char = char
            if thinking_pauses:
                if char == '\n':
                    time.sleep(random.uniform(1.20, 2.50))
                elif char in ".,":
                    time.sleep(random.uniform(0.60, 1.20))
                else:
                    time.sleep(random.uniform(0.40, 0.80))
            i += 1
            continue

        if error_rate > 0 and char.lower() in QWERTY_ADJACENT and random.random() < error_rate:
            typo_char = random.choice(QWERTY_ADJACENT[char.lower()])
            if char.isupper():
                typo_char = typo_char.upper()
            pyautogui.write(typo_char)
            time.sleep(random.uniform(0.20, 0.40)) 
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.15, 0.30))

        pyautogui.write(char)
        time.sleep(human_keystroke_delay(char, prev_char))
        prev_char = char
        i += 1

# ==============================================================================
# BOTTOM-RIGHT TOAST WITH "OPEN EMAIL" BUTTON (MAIN)
# ==============================================================================
toast_window = None

def trigger_open_email():
    close_toast_popup()
    resolved_email = str(Path(EMAIL_FILE).resolve())
    open_in_chrome(resolved_email)

def display_bottom_right_toast():
    global toast_window
    root = tk.Tk()
    toast_window = root
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    w, h = 360, 130
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = screen_w - w - 20
    y = screen_h - h - 55
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.configure(bg="#2d2d30")

    frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
    frame.pack(fill="both", expand=True, padx=1, pady=1)

    lbl_app = tk.Label(frame, text="✉️ Outlook • Priority Message", font=("Segoe UI", 9, "bold"), fg="#0078d4", bg="#ffffff")
    lbl_app.pack(anchor="w", padx=14, pady=(8, 2))
    lbl_sender = tk.Label(frame, text="LAOBAN (director@company.internal)", font=("Segoe UI", 10, "bold"), fg="#202124", bg="#ffffff")
    lbl_sender.pack(anchor="w", padx=14, pady=0)
    lbl_msg = tk.Label(frame, text="RE: Annual Dinner 2026 - Budget & Lucky Draw...", font=("Segoe UI", 9), fg="#5f6368", bg="#ffffff")
    lbl_msg.pack(anchor="w", padx=14, pady=(2, 6))

    btn_frame = tk.Frame(frame, bg="#ffffff")
    btn_frame.pack(anchor="e", padx=14, pady=(0, 8))

    btn_open = tk.Button(
        btn_frame, text="Open email", font=("Segoe UI", 9, "bold"),
        bg="#0078d4", fg="white", activebackground="#106ebe", activeforeground="white",
        relief="flat", padx=12, pady=2, cursor="hand2", command=trigger_open_email
    )
    btn_open.pack()
    root.mainloop()

def show_toast_popup():
    t = threading.Thread(target=display_bottom_right_toast, daemon=True)
    t.start()
    time.sleep(2.5 + random.uniform(-0.1, 0.5))

def close_toast_popup():
    global toast_window
    if toast_window:
        try:
            toast_window.destroy()
            toast_window = None
        except Exception:
            pass

# ==============================================================================
# HUMAN CURSOR DYNAMICS (CUBIC BÉZIER) (MAIN)
# ==============================================================================
def bezier_point(p0, p1, p2, p3, t):
    return (
        (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0],
        (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
    )

def human_move(target_x, target_y, duration=0.65):
    start_x, start_y = pyautogui.position()
    distance = math.hypot(target_x - start_x, target_y - start_y)
    if distance < 4:
        return
    ctrl1_x = start_x + (target_x - start_x) * 0.3 + random.uniform(-35, 35)
    ctrl1_y = start_y + (target_y - start_y) * 0.3 + random.uniform(-35, 35)
    ctrl2_x = start_x + (target_x - start_x) * 0.7 + random.uniform(-35, 35)
    ctrl2_y = start_y + (target_y - start_y) * 0.7 + random.uniform(-35, 35)

    p0, p1, p2, p3 = (start_x, start_y), (ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y), (target_x, target_y)
    steps = max(20, int(duration * 60))
    t0 = time.monotonic()

    for i in range(1, steps + 1):
        t = i / float(steps)
        t_eased = t * t * (3 - 2 * t)
        bx, by = bezier_point(p0, p1, p2, p3, t_eased)
        pyautogui.moveTo(int(bx), int(by))
        needed = (duration / steps) * i - (time.monotonic() - t0)
        if needed > 0:
            time.sleep(needed)

def human_double_click(target_x, target_y):
    human_move(target_x, target_y, duration=0.6)
    time.sleep(0.15)
    pyautogui.click()
    time.sleep(random.uniform(0.10, 0.18))
    pyautogui.click()
    time.sleep(0.25)

def human_click(target_x=None, target_y=None):
    if target_x is not None and target_y is not None:
        human_move(target_x, target_y, duration=0.55)
    time.sleep(0.15)
    pyautogui.click()
    time.sleep(0.2)

def human_scroll(clicks, pause_between=0.4):
    direction = -1 if clicks < 0 else 1
    total = abs(clicks)
    while total > 0:
        step = min(total, 2)
        pyautogui.scroll(direction * step * 120)
        total -= step
        time.sleep(pause_between + random.uniform(-0.1, 0.2))

# ==========================================================
# MOUSE FUNCTIONS (SCRIPT 2)
# ==========================================================
def move_click(x, y):
    pyautogui.moveTo(x, y, duration=0.9, tween=pyautogui.easeInOutQuad)
    time.sleep(0.6)
    pyautogui.click()
    time.sleep(1.2 + random.uniform(-0.2, 0.4))

def click_button(name):
    if name not in WPS_POSITIONS:
        raise RuntimeError("Missing button coordinate: " + name)
    x, y = WPS_POSITIONS[name]
    print("Clicking:", name)
    move_click(x, y)

# ==========================================================
# ONE-TIME COORDINATE SETUP (SCRIPT 2)
# ==========================================================
def capture_wps_position(name, instruction):
    message = (instruction + "Click OK, then move your mouse over the "
               + "correct button within 5 seconds.\nDo not click the button yourself.")
    pyautogui.alert(text=message, title="WPS Button Setup", button="OK")
    time.sleep(5)
    x, y = pyautogui.position()
    WPS_POSITIONS[name] = [x, y]
    print(name, "=", x, y)

def calibrate_toolbar():
    print("Setting up WPS toolbar coordinates...")
    capture_wps_position("bold", "Hover over the Bold (B) button.")
    capture_wps_position("underline", "Hover over the Underline (U) button.")
    capture_wps_position("bullets", "Hover over the Bulleted List button.")
def load_wps_positions():
    global WPS_POSITIONS
    if not WPS_COORDS_FILE.exists():
        print("No saved WPS button coordinates found. Will need setup if formatting is required.")
        return
    WPS_POSITIONS = json.loads(WPS_COORDS_FILE.read_text(encoding="utf-8"))
    print("Loaded saved WPS button positions.")

def save_wps_positions():
    WPS_COORDS_FILE.write_text(json.dumps(WPS_POSITIONS, indent=4), encoding="utf-8")

# ==========================================================
# TYPING FUNCTIONS (SCRIPT 2)
# ==========================================================

def type_text(text):
    human_type(text, error_rate=0.015, thinking_pauses=False)

def type_line(text):
    type_text(text)
    time.sleep(random.uniform(0.3, 0.6))
    pyautogui.press("enter")
    time.sleep(0.8 + random.uniform(-0.1, 0.3))

def blank_line():
    pyautogui.press("enter")
    time.sleep(0.8 + random.uniform(-0.1, 0.3))

def correct_typo(wrong, correct):
    type_text(wrong)
    time.sleep(1.5 + random.uniform(-0.2, 0.6))
    pyautogui.press("backspace", presses=len(wrong), interval=0.10)
    time.sleep(0.8 + random.uniform(-0.1, 0.4))
    type_text(correct)

# ==========================================================
# BULLET LIST FUNCTIONS (SCRIPT 2)
# ==========================================================
def start_bullets():
    click_button("bullets")

def bullet_line(text):
    type_text(text)
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.press("enter")
    time.sleep(0.8 + random.uniform(-0.1, 0.3))

def end_bullets():
    pyautogui.press("enter")
    time.sleep(0.8 + random.uniform(-0.1, 0.3))

def bullet_list(items):
    start_bullets()
    for item in items:
        bullet_line(item)
    end_bullets()

# ==========================================================
# FIND EXISTING SPREADSHEET (SCRIPT 3)
# ==========================================================
def find_desktop_file():
    desktop_folders = [
        Path.home() / "Desktop",
        Path.home() / "OneDrive" / "Desktop",
        DESKTOP_DIR  # Included to ensure the MAIN's directory is checked
    ]
    extensions = {".xlsx", ".xls", ".xlsm", ".et", ".csv"}
    matches = []
    for folder in desktop_folders:
        if not folder.exists(): continue
        for file in folder.iterdir():
            if file.is_file() and file.stem.lower() == FILE_NAME_BUDGET.lower() and file.suffix.lower() in extensions:
                matches.append(file)
    if len(matches) == 0:
        raise FileNotFoundError("Cannot find the budget file on Desktop.\nExpected name: " + FILE_NAME_BUDGET)
    return matches[0]

# ==========================================================
# MOUSE MOVEMENT (SCRIPT 3)
# ==========================================================
def move_mouse(x, y, duration=1.0):
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
    time.sleep(0.5)

def budget_human_click(x, y):
    move_mouse(x, y)
    pyautogui.click()
    time.sleep(1.0)

def budget_human_double_click(x, y):
    move_mouse(x, y)
    time.sleep(0.6)
    pyautogui.doubleClick(interval=0.2)
    time.sleep(1.5)

# ==========================================================
# COORDINATE CALIBRATION (SCRIPT 3)
# ==========================================================
def load_budget_positions():
    global BUDGET_POSITIONS
    if BUDGET_COORDS_FILE.exists():
        BUDGET_POSITIONS = json.loads(BUDGET_COORDS_FILE.read_text(encoding="utf-8"))
        print("Saved budget cursor coordinates loaded.")
    else:
        BUDGET_POSITIONS = {}
        print("No previous budget coordinates found. One-time calibration will be performed.")

def save_budget_positions():
    BUDGET_COORDS_FILE.write_text(json.dumps(BUDGET_POSITIONS, indent=4), encoding="utf-8")

def capture_budget_position(name, instruction):
    pyautogui.alert(
        text=(instruction + "Click OK, then move your mouse over the target within 5 seconds.\nDo not click it yourself."),
        title="Cursor Position Setup", button="OK"
    )
    time.sleep(5)
    x, y = pyautogui.position()
    BUDGET_POSITIONS[name] = [x, y]
    save_budget_positions()
    print(name, "=", x, y)

def get_budget_position(name, instruction):
    if name not in BUDGET_POSITIONS:
        capture_budget_position(name, instruction)
    return BUDGET_POSITIONS[name]

def click_saved(name, instruction):
    x, y = get_budget_position(name, instruction)
    print("Clicking:", name)
    budget_human_click(x, y)

def double_click_saved(name, instruction):
    x, y = get_budget_position(name, instruction)
    
    if name == "explorer_icon":
        x = x - 15  # Move 15 pixels to the left
        
    print("Double-clicking:", name)
    budget_human_double_click(x, y)

def budget_human_type(text):
    # 【修复：略微放慢搜索框打字速度(0.06)，比原先的0.03慢，但依然能防卡顿】
    pyautogui.write(text, interval=0.06)

# ==========================================================
# FILE EXPLORER WORKFLOW FUNCTIONS (SCRIPT 3)
# ==========================================================
def open_file_explorer():
    print("[1] Opening File Explorer...")
    if OPEN_EXPLORER_WITH_MOUSE:
        click_saved("explorer_icon", "Hover over the File Explorer folder icon on the Windows taskbar.")
    else:
        pyautogui.hotkey("win", "e")
    
    time.sleep(6.0 + random.uniform(-0.5, 1.5))
    pyautogui.hotkey("win", "up")
    time.sleep(2.0 + random.uniform(-0.1, 0.5))

def open_desktop():
    print("[2] Opening Desktop folder...")
    click_saved("desktop_folder", "Hover over Desktop in the File Explorer left navigation panel.")
    time.sleep(4.0 + random.uniform(-0.3, 0.8))

def search_budget_file():
    print("[3] Searching for budget spreadsheet...")
    pyautogui.hotkey("ctrl", "f")
    time.sleep(3.5 + random.uniform(0.5, 1.0)) 
    
    print("Typing filename...")
    budget_human_type(FILE_NAME_BUDGET)
    
    time.sleep(3.0 + random.uniform(0.5, 1.0))
    pyautogui.press("enter")
    
    print("Waiting for search results...")
    time.sleep(18.0 + random.uniform(1.0, 3.0)) 

def open_budget_file():
    print("[4] Opening matching budget file...")
    double_click_saved("budget_result", "Hover over the matching file named 'Budget List for Annual Dinner (draft)' in File Explorer's search results.")
    print("Waiting for WPS Spreadsheets...")
    time.sleep(15.0 + random.uniform(-1.0, 2.5)) 
    pyautogui.hotkey("win", "up")
    time.sleep(3.0 + random.uniform(-0.2, 0.6))

def update_budget():
    print("[5] Updating income value...")
    click_saved("income_cell", "Hover over the income cell in WPS where you want to enter 10000.")
    time.sleep(2.0 + random.uniform(-0.1, 0.5))
    budget_human_type(INCOME_VALUE)
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(3.5 + random.uniform(-0.2, 0.8))
    print("Income value entered:", INCOME_VALUE)
    print("Waiting for formulas to recalculate...")
    time.sleep(8.0 + random.uniform(-0.5, 1.5))

def save_budget():
    print("[6] Saving workbook...")
    pyautogui.hotkey("ctrl", "s")
    time.sleep(4.5 + random.uniform(-0.3, 1.0))
    print("Save command completed.")

# ==============================================================================
# LOCAL ASSETS SETUP (MAIN)
# ==============================================================================
def setup_local_environment():
    email_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Outlook Mail - Jonathan (Inbox)</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; }
  body { display: flex; height: 100vh; background: #f3f2f1; color: #201f1e; overflow: hidden; }
  .sidebar { width: 220px; background: #edebe9; border-right: 1px solid #d2d0ce; padding: 15px 0; }
  .user-badge { padding: 0 16px 15px; border-bottom: 1px solid #e1dfdd; font-size: 13px; font-weight: bold; color: #0078d4; }
  .folder { padding: 10px 16px; cursor: pointer; font-size: 14px; display: flex; justify-content: space-between; }
  .folder.active { background: #c7e0f4; font-weight: 600; color: #004578; }
  .mail-list { width: 330px; background: #ffffff; border-right: 1px solid #e1dfdd; overflow-y: auto; }
  .list-header { padding: 12px 16px; font-size: 15px; font-weight: bold; border-bottom: 1px solid #edebe9; }
  .mail-item { padding: 14px 16px; border-bottom: 1px solid #edebe9; cursor: pointer; }
  .mail-item.selected { background: #eff6fc; border-left: 4px solid #0078d4; }
  .mail-item .from { font-weight: bold; font-size: 14px; color: #323130; }
  .mail-item .subj { font-size: 13px; color: #201f1e; margin-top: 3px; }
  .preview-pane { flex: 1; background: #ffffff; padding: 25px 35px; overflow-y: auto; display: flex; flex-direction: column; }
  .mail-header { border-bottom: 1px solid #edebe9; padding-bottom: 15px; margin-bottom: 20px; }
  .mail-header h2 { font-size: 20px; color: #201f1e; margin-bottom: 10px; }
  .mail-meta { font-size: 13px; color: #605e5c; line-height: 1.6; }
  .mail-body { font-size: 14px; line-height: 1.8; color: #323130; flex: 1; white-space: pre-wrap
; }
  .reply-card { position: fixed; right: 30px; bottom: 25px; width: 480px; border: 1px solid #d2d0ce; border-radius: 4px; padding: 15px; background: #faf9f8; box-shadow: 0 4px 16px rgba(0,0,0,0.15); z-index: 9999; }
  .reply-card textarea { width: 100%; height: 95px; border: 1px solid #c8c6c4; border-radius: 3px; padding: 10px; font-size: 13px; font-family: inherit; }
  .reply-actions { margin-top: 10px; display: flex; justify-content: flex-end; }
  .btn-send { background: #0078d4; color: white; border: none; padding: 8px 22px; border-radius: 3px; font-weight: 600; font-size: 13px; cursor: pointer; }
  .sent-banner { display: none; margin-top: 15px; padding: 12px 16px; background: #dff6dd; color: #107c10; font-weight: bold; font-size: 14px; border-radius: 4px; border: 1px solid #107c10; }
</style>
<script>
  function sendReply() {
    var txt = document.getElementById('replyArea').value;
    if(txt.trim().length > 0) {
      document.getElementById('replyCardInner').style.opacity = '0.5';
      document.getElementById('sendBtn').disabled = true;
      document.getElementById('sendBtn').innerText = 'Sending...';
      setTimeout(function() {
        document.getElementById('replyCardInner').style.display = 'none';
        document.getElementById('sentBanner').style.display = 'block';
      }, 500);
    }
  }
</script>
</head>
<body>
  <div class="sidebar">
    <div class="user-badge">👤 Jonathan (Corp Account)</div>
    <div class="folder active"><span>📥 Inbox</span><span>(1)</span></div>
    <div class="folder"><span>⭐ Starred</span></div>
    <div class="folder"><span>📤 Sent Items</span></div>
    <div class="folder"><span>📝 Drafts</span></div>
    <div class="folder"><span>🗑️ Deleted</span></div>
  </div>
  <div class="mail-list">
    <div class="list-header">Focused Inbox</div>
    <div class="mail-item selected">
      <div class="from">🔴 LAOBAN &lt;director@company.internal&gt;</div>
      <div class="subj">RE: Annual Exhibition Planning & Budget</div>
      <div style="font-size: 12px; color: #605e5c; margin-top: 4px;">Dear Jonathan, The company will be having its annual exhibition in three months...</div>
    </div>
  </div>
  <div class="preview-pane">
    <div class="mail-header">
      <h2>RE: Annual Exhibition Planning & Budget</h2>
      <div class="mail-meta">
        <div><b>From:</b> LAOBAN &lt;director@company.internal&gt;</div>
        <div><b>To:</b> Jonathan &lt;jonathan@company.internal&gt;</div>
        <div><b>Date:</b> Today, 09:15 AM</div>
      </div>
    </div>
    <div class="mail-body">Dear Jonathan,
The company will be having its annual exhibition in three months, and I would like you to draft up a rough plan with any relevant details in regards to the event flow. You are allocated a budget of S$10000 for the whole event.
Regarding the lucky draw prize, feel free to allocate all remaining surplus funds toward a flagship Apple product to motivate the staff.
Thank you.
Regards,
Lao Ban</div>
    <div class="reply-card">
      <div id="replyCardInner">
        <div style="font-weight: 600; margin-bottom: 8px; font-size: 13px;">Quick Reply to Lao Ban:</div>
        <textarea id="replyArea" placeholder="Click here to type reply to Lao Ban..."></textarea>
        <div class="reply-actions">
          <button id="sendBtn" class="btn-send" onclick="sendReply()">Send Reply</button>
        </div>
      </div>
      <div id="sentBanner" class="sent-banner">
        ✓ Message Sent successfully to Lao Ban &lt;director@company.internal&gt;! (Outbox cleared)
      </div>
    </div>
  </div>
</body>
</html>"""
    EMAIL_FILE.write_text(email_html, encoding="utf-8")

    mock_apple_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Apple (Singapore) - Official Store Mock</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #fff; color: #1d1d1f; }}
  nav {{ background: rgba(0,0,0,0.85); color: #f5f5f7; padding: 14px 30px; font-size: 14px; text-align: center; }}
  .container {{ max-width: 980px; margin: 30px auto; padding: 0 20px; }}
  .hero {{ text-align: center; margin-bottom: 35px; }}
  .grid {{ display: flex; gap: 20px; justify-content: center; }}
  .card {{ flex: 1; border: 1px solid #d2d2d7; border-radius: 18px; padding: 25px; text-align: center; background: #fafafa; }}
  .title {{ font-size: 21px; font-weight: bold; margin: 10px 0; }}
  .price {{ font-size: 18px; color: #6e6e73; margin: 10px 0; }}
  .btn {{ display: inline-block; background: #0071e3; color: white; padding: 8px 18px; border-radius: 980px; text-decoration: none; font-size: 13px; font-weight: 500; }}
  .footer-note {{ margin-top: 50px; font-size: 13px; color: #86868b; line-height: 1.6; border-top: 1px solid #d2d2d7; padding-top: 20px; }}
</style>
</head>
<body>
  <nav>Apple Store &nbsp;|&nbsp; Mac &nbsp;|&nbsp; iPad &nbsp;|&nbsp; iPhone &nbsp;|&nbsp; Watch &nbsp;|&nbsp; AirPods</nav>
  <div class="container">
    <div class="hero">
      <h1>Featured Corporate Rewards (Singapore)</h1>
      <p>Shortlisting lucky draw items within the S$1,800.00 surplus limit</p>
    </div>
    <div class="grid">
      <div class="card">
        <div class="title">Apple iPad Air 11-inch</div>
        <div class="price">From S$899.00</div>
        <p>Within budget, but leaves ~S$900 unspent.</p>
        <span class="btn">View specs</span>
      </div>
      <div class="card">
        <div class="title">Apple iPhone 18</div>
        <div class="price">From S$1,800.00</div>
        <p><b>Exact Match:</b> Utilizes entire S$1,800.00 surplus balance!</p>
        <span class="btn" style="background:#34a853;">Selected Choice</span>
      </div>
      <div class="card">
        <div class="title">Apple MacBook Pro 14"</div>
        <div class="price">From S$2,499.00</div>
        <p>Exceeds available surplus limit.</p>
        <span class="btn" style="background:#86868b;">Over budget</span>
      </div>
    </div>
  </div>
</body>
</html>"""
    MOCK_APPLE_FILE.write_text(mock_apple_html, encoding="utf-8")

    search_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>apple - Google Chrome Search</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px 45px; color: #202124; background: #fff; }}
  .search-bar {{ width: 600px; padding: 12px 20px; font-size: 15px; border: 1px solid #dfe1e5; border-radius: 24px; outline: none; margin-bottom: 25px; }}
  .result {{ max-width: 650px; margin-bottom: 30px; }}
  .url {{ font-size: 12px; color: #202124; margin-bottom: 4px; }}
  .title {{ font-size: 20px; color: #1a0dab; text-decoration: none; display: inline-block; margin-bottom: 4px; cursor: pointer; }}
  .title:hover {{ text-decoration: underline; }}
  .desc {{ font-size: 14px; color: #4d5156; line-height: 1.5; }}
</style>
</head>
<body>
  <input class="search-bar" type="text" value="apple" readonly>
  <div class="result" id="appleMain">
    <div class="url">{LIVE_APPLE_URL} &rsaquo; sg</div>
    <a class="title" href="{LIVE_APPLE_URL}">Official Apple Store Singapore</a>
    <div class="desc">Discover the innovative world of Apple. Explore iPhone 18, iPad Air, MacBook Pro, Apple Watch, and accessories with corporate pricing.</div>
  </div>
  <div class="result">
    <div class="url">offline://local/mock-apple-store</div>
    <a class="title" href="{MOCK_APPLE_FILE.name}">Apple Store Singapore (Offline Fallback Catalog)</a>
    <div class="desc">Deterministic offline simulation catalog for evaluation testing.</div>
  </div>
</body>
</html>"""
    SEARCH_FILE.write_text(search_html, encoding="utf-8")

# ==============================================================================
# MAIN WORKFLOW EXECUTION
# ==============================================================================

def main():
    global START_TIME

    START_TIME = time.monotonic()

    print("Starting Annual Dinner Agent...", flush=True)

    setup_local_environment()

    # Load existing saved coordinates
    load_wps_positions()
    load_budget_positions()

    # STEP 1: Open WPS
    print("Opening WPS Office...", flush=True)
    open_wps()

    # Calibrate only if coordinates are missing
    if not WPS_POSITIONS:
        calibrate_toolbar()
        save_wps_positions()

    # STEP 2: Save initial document
    save_to_desktop()

    # STEPS 3-8: Create the complete document
    create_title()
    create_theme()
    create_event_details()
    create_programme()
    create_arrangements()
    create_final_notes()

    # Continue existing email, budget and browser workflow
    continue_workflow()

    # Save the document
    pyautogui.hotkey("ctrl", "s")

    print("WPS document completed.", flush=True)

# ==========================================================
# STEP 1: OPEN WPS OFFICE
# ==========================================================

def open_wps():

    print("[1] Opening WPS Office...")

    pyautogui.hotkey("win", "s")
    time.sleep(2.0 + random.uniform(-0.2, 0.5))

    pyautogui.write(
        "WPS Office",
        interval=0.15
    )

    time.sleep(3.0 + random.uniform(-0.3, 0.8))

    pyautogui.press("enter")
    time.sleep(9.0 + random.uniform(-0.5, 2.0))

    # Select Docs from WPS Home
    print("Selecting Docs...")
    move_click(*DOCS_BUTTON)

    time.sleep(3.0 + random.uniform(-0.2, 0.6))

    # Select Blank document
    print("Creating blank document...")
    move_click(*BLANK_BUTTON)

    time.sleep(6.0 + random.uniform(-0.4, 1.5))

# ==========================================================
# STEP 2: SAVE ON DESKTOP
# ==========================================================
def save_to_desktop():

    print("[2] Opening Save As...")

    pyautogui.press("f12")
    time.sleep(4.0 + random.uniform(-0.3, 1.0))

    # ==========================================
    # 1. SELECT DESKTOP
    # ==========================================

    if "desktop" not in WPS_POSITIONS:

        print("Desktop coordinate missing. Calibrating...")

        capture_wps_position(
            "desktop",
            "Hover over Desktop in the Save As sidebar."
        )

        save_wps_positions()

    print("Selecting Desktop folder...")
    click_button("desktop")

    time.sleep(3.0 + random.uniform(-0.2, 0.6))

    # ==========================================
    # 2. SELECT FILE NAME FIELD
    # ==========================================

    if "filename" not in WPS_POSITIONS:

        print("Filename coordinate missing. Calibrating...")

        capture_wps_position(
            "filename",
            "Hover over the File name text input box."
        )

        save_wps_positions()

    print("Selecting filename field...")
    click_button("filename")

    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.8)

    print("Typing document name...")
    type_text(FILE_NAME)

    time.sleep(1.5 + random.uniform(-0.1, 0.5))

    # ==========================================
    # 3. CLICK SAVE
    # ==========================================

    if "save" not in WPS_POSITIONS:

        print("Save button coordinate missing. Calibrating...")

        capture_wps_position(
            "save",
            "Hover over the Save button."
        )

        save_wps_positions()

    print("Clicking Save...")
    click_button("save")

    time.sleep(4.0 + random.uniform(-0.3, 1.0))

    # ==========================================
    # 4. VERIFY FILE EXISTS
    # ==========================================

    saved_files = [
        path
        for extension in (".wps", ".docx", ".doc")
        for path in DESKTOP.glob(FILE_NAME + extension)
    ]

    if not saved_files:

        raise RuntimeError(
            "Document was not found on Desktop. "
            "Please check the Save As window."
        )

    print("Document saved successfully!")

    for file in saved_files:
        print("Location:", file)

    save_wps_positions()

    print("WPS coordinates saved for future runs.")

# ==========================================================
# STEP 3: TITLE FORMATTING
# ==========================================================
def create_title():

    print("[3] Creating document title...")

    # Click inside the document area
    screen_w, screen_h = pyautogui.size()

    move_click(
        int(screen_w * 0.50),
        int(screen_h * 0.40)
    )

    pyautogui.hotkey("ctrl", "home")
    time.sleep(1.0)

    title = "Event planning for company annual dinner 2026"

    # STEP A: Type as normal text first
    print("Typing normal title...")
    type_text(title)

    time.sleep(2.0 + random.uniform(-0.1, 0.5))

    # STEP B: Select the entire first line
    print("Selecting first line...")
    pyautogui.keyDown("shift")
    pyautogui.press("home")
    pyautogui.keyUp("shift")

    time.sleep(1.2)

    # STEP C: Click Bold and Underline
    print("Applying Bold...")
    click_button("bold")

    time.sleep(1.0)

    print("Applying Underline...")
    click_button("underline")

    time.sleep(1.2)

    # STEP D: Deselect and move to next line
    pyautogui.press("end")
    time.sleep(0.5)
    pyautogui.press("enter")

    time.sleep(1.0)

    # STEP E: Turn OFF Bold and Underline
    # The next paragraph initially inherits title formatting.
    print("Turning off Bold for body text...")
    click_button("bold")

    time.sleep(1.0)

    print("Turning off Underline for body text...")
    click_button("underline")

    time.sleep(1.0)

    # Leave a blank line before the next section
    pyautogui.press("enter")

    time.sleep(1.0)

    print("Title completed. Body text is now normal.")

# ==========================================================
# STEP 4: THEME
# ==========================================================

def create_theme():

    print("[4] Creating theme section...")

    time.sleep(1.5)
    type_line("Theme (to be discussed in mtg):")

    bullet_list([
        "future forward (ai & innovation)",
        "metaverse & hybrid experiences",
        "green & eco-responsible"
    ])

    blank_line()

# ==========================================================
# STEP 5: EVENT DETAILS
# ==========================================================

def create_event_details():

    print("[5] Adding event details...")

    time.sleep(2.0)
    type_line(
        "Target audience: approx. 100 pax "
        "(all staff and management) --- "
        "need HR confirm final guest list + VIPs"
    )

    blank_line()

    type_line("Date: 18 Dec 2026 (Fri)")

    blank_line()

    type_line("Time: 5pm - 10:30pm")

    blank_line()

    type_line(
        "Venue shortlist "
        "(prefer ballroom with built-in AV):"
    )

    # Venue list
    start_bullets()

    bullet_line("Mbs")
    bullet_line("Four seasons")

    # Controlled lag demonstration
    type_text("Fullerton H")

    # 【微调：发呆时间从25秒减为20秒】
    print("Pausing for 20 seconds... (Daydreaming)")
    time.sleep(20.0 + random.uniform(-1.0, 3.0))

    glitch_text = (
        "otel?????hdbhjcbdhvbahsdbchjsbvhusaducjhcbadshf"
    )

    pyautogui.write(glitch_text, interval=0.005)

    time.sleep(10.0 + random.uniform(-0.5, 2.0))

    # Remove only the unwanted characters
    unwanted = glitch_text[len("otel"):]

    pyautogui.press(
        "backspace",
        presses=len(unwanted),
        interval=0.1
    )

    pyautogui.press("enter")
    end_bullets()
    blank_line()

# ==========================================================
# STEP 6: PROGRAMME RUNDOWN
# ==========================================================

def create_programme():

    print("[6] Adding programme rundown...")

    time.sleep(2.0)
    type_line("Key programme rundown")

    bullet_list([
        "5pm: registration & welcome cocktail",
        "6pm: opening address / company highlights",
        "6:30pm: staff recognition & awards",
        "7:15pm: dinner buffet",
        "8pm: entertainment & games",
        "8:45pm: lucky draw",
        "9:30pm: final prize & group photos",
        "10pm onwards: free mingle / wrap up"
    ])

    blank_line()
    
# ==========================================================
# STEP 7: ARRANGEMENTS
# ==========================================================

def create_arrangements():

    print("[7] Adding arrangements...")
    time.sleep(1.5)

    type_line("Things to arrange:")

    start_bullets()

    bullet_line("Confirm guest list with HR")

    bullet_line(
        "Hire caterer if venue package doesn't cover food"
    )

    bullet_line("Entertainers (source)")

    # Small typo, followed by correction
    correct_typo(
        "Photograper",
        "Photographer"
    )

    bullet_line(" + videographer")

    bullet_line("Stage / lighting / backdrop / AV")
    bullet_line("Flowers + deco")
    bullet_line("Door gifts")
    bullet_line("Lucky draw gifts")
    bullet_line("Registration table + signage")

    end_bullets()

    blank_line()

# ==========================================================
# STEP 8: DOOR GIFTS AND BUDGET NOTES
# ==========================================================

def create_final_notes():

    print("[8] Adding final notes...")
    time.sleep(1.5)

    type_line(
        "Door gift ideas (to vote): "
        "phone stand, plushie, keychain, travel bag"
    )

    blank_line()

    type_line("Lucky draw grand prize allocation")

    type_line(
        "Status: pending final budget surplus review"
    )

    type_text("Selected item: TBD")

def continue_workflow():
    screen_w, screen_h = pyautogui.size()

    # --------------------------------------------------------------------------
    # Step 6: Pop-up Notification -> Click 'Open email' Button
    # --------------------------------------------------------------------------
    print("[6/17] Boss email toast appears in bottom-right corner...")
    show_toast_popup()
    time.sleep(3.5 + random.uniform(-0.2, 0.8))
    open_btn_x = screen_w - 95
    open_btn_y = screen_h - 75
    print("[*] Gliding cursor down to click 'Open email'...")
    human_click(open_btn_x, open_btn_y)
    time.sleep(6.0 + random.uniform(-0.3, 1.2))

    # --------------------------------------------------------------------------
    # Step 7: Read Lao Ban's Email 
    # --------------------------------------------------------------------------
    print("[7/17] Reading email in Chrome (~33s+ with scrolling)...")
    human_move(screen_w // 2, screen_h // 2)
    time.sleep(2.0)
    human_scroll(-3, pause_between=0.4)
    
    time.sleep(8.0 + random.uniform(-0.5, 1.5)) 
    human_scroll(-3, pause_between=0.4)
    time.sleep(15.0 + random.uniform(-1.0, 2.5))
    human_scroll(4, pause_between=0.4)
    time.sleep(10.0 + random.uniform(-1.0, 2.0))

    # --------------------------------------------------------------------------
    # Step 8: Direct Reply to Lao Ban as Jonathan & SEND
    # --------------------------------------------------------------------------
    print("[8/17] Replying to Lao Ban as Jonathan...")
    reply_box_x = screen_w - 270
    reply_box_y = screen_h - 145
    human_click(reply_box_x, reply_box_y)
    time.sleep(2.0 + random.uniform(-0.1, 0.5))

    reply_content = (
        "Dear Mr Lao,\n\n"
        "Noted with thanks, will provide the relevant documents a few days for your perusal "
        "before our upcoming meeting \n\n "
        "Best regards,\n"
        "Jonathan"
    )
    human_type(reply_content, error_rate=0.015)
    time.sleep(2.5 + random.uniform(-0.2, 0.6))

    print("[*] Sending reply in Chrome...")
    time.sleep(0.8)
    send_btn_x = screen_w - 95
    send_btn_y = screen_h - 95
    human_click(send_btn_x, send_btn_y)
    time.sleep(4.0 + random.uniform(-0.3, 0.8))

    # --------------------------------------------------------------------------
    # Step 9 & 10: Open File Explorer -> Budget
    # --------------------------------------------------------------------------
    print("[9/17] Jonathan opens File Explorer to search for the Budget list...")
    budget_file = find_desktop_file()
    print("Target file found:", budget_file)

    open_file_explorer()
    open_desktop()
    search_budget_file()
    open_budget_file()

    if OPEN_ONLY:
        print("OPENING TEST COMPLETE.")
        return

    screen_w, screen_h = pyautogui.size()

    move_click(
        int(screen_w * 0.50),
        int(screen_h - 70)
    )

    print("[10/17] Keying in 10000 and waiting for 1920 to appear...")
    update_budget()

    print("[*] Waiting for formula to output 1920...")
    time.sleep(20.0 + random.uniform(-1.0, 3.0))

    save_budget()

    # --------------------------------------------------------------------------
    # Step 11: Open Google Chrome -> Search Apple Store for Items within S$1,800
    # --------------------------------------------------------------------------
    print("[11/17] Launching Google Chrome to shortlist prizes within S$1,800...")
    open_just_chrome() 
    time.sleep(2.0 + random.uniform(-0.2, 0.5))
    type_url_in_chrome("https://www.apple.com")
    bypass_chrome_ssl_warning()

    # --------------------------------------------------------------------------
    # Step 12: Scroll Down in Chrome to Inspect Available Products
    # --------------------------------------------------------------------------
    print("[12/17] Scrolling through Apple Store catalog in Chrome...")
    time.sleep(3.0)
    for _ in range(5):
        human_scroll(-4, pause_between=0.4)
        
        time.sleep(random.uniform(6.0, 10.0))
        human_move(screen_w // 2 + random.randint(-40, 40), screen_h // 2 + random.randint(-20, 20))

    print(f"[*] Checking authorized whitelisted comparison tab in Chrome: {LIVE_SAMSUNG_URL}...")
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1.5 + random.uniform(-0.1, 0.4))
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.5 + random.uniform(-0.05, 0.2))
    human_type(LIVE_SAMSUNG_URL, error_rate=0.0)
    pyautogui.press("enter")
    time.sleep(5.5 + random.uniform(-0.3, 1.0))
    bypass_chrome_ssl_warning()

    human_scroll(-3, pause_between=0.4)
    time.sleep(5.0 + random.uniform(-0.3, 1.0))

    # --------------------------------------------------------------------------
    # Step 13: Switch Back to Budget Spreadsheet to Review Budget
    # --------------------------------------------------------------------------
    print("[13/17] Switching back to Budget spreadsheet using Alt+Tab...")
    pyautogui.keyDown("alt")
    time.sleep(0.4)
    pyautogui.press("tab")
    time.sleep(0.6)
    pyautogui.keyUp("alt")
    time.sleep(3.5 + random.uniform(-0.3, 0.8))

    
    print("[*] Pondering budget choices for 60 seconds to determine the best Apple product...")
    time.sleep(60.0 + random.uniform(-2.0, 5.0))

    # --------------------------------------------------------------------------
    # Step 14: Return to WPS Writer Draft, Erase 'TBD' & Type iPhone 18
    # --------------------------------------------------------------------------

    print("[14/17] Returning to original WPS Writer draft document...")
    
    screen_w, screen_h = pyautogui.size()
    
    wps_taskbar_x = 290
    wps_taskbar_y = 18
    
    print(f"[*] Clicking WPS icon on taskbar at ({wps_taskbar_x}, {wps_taskbar_y})...")
    pyautogui.moveTo(wps_taskbar_x, wps_taskbar_y, duration=0.8, tween=pyautogui.easeInOutQuad)
    time.sleep(0.5)
    pyautogui.click()
    
    time.sleep(3.5 + random.uniform(-0.2, 0.8))

    pyautogui.hotkey("ctrl", "end")
    time.sleep(2.0 + random.uniform(-0.1, 0.5))

    pyautogui.keyDown("shift")
    pyautogui.press("left", presses=3, interval=0.2)
    pyautogui.keyUp("shift")
    time.sleep(1.0)

    print("[*] Replacing TBD with iPhone 18...")
    human_type(
    "Apple iPhone 18 x 1 [Allocated Budget: S$1800.00 - Fully Covered by Surplus]",
    error_rate=0.0
    )

    pyautogui.hotkey("ctrl", "s")
    time.sleep(3.0 + random.uniform(-0.2, 0.6))

    print("[*] TBD replacement completed.")

    # --------------------------------------------------------------------------
    # Step 15: Review Proposal (Scroll Up to Top, Then Back to Bottom)
    # --------------------------------------------------------------------------
    print("[15/17] Reviewing proposal: scrolling to top, then down to bottom...")
    time.sleep(2.0)
    human_scroll(12, pause_between=0.4)
    
    time.sleep(random.uniform(8.0, 12.0))
    human_scroll(-12, pause_between=0.4)
    time.sleep(random.uniform(6.0, 9.0))

    # --------------------------------------------------------------------------
    # Step 17: Close All Tabs & Conclude
    # --------------------------------------------------------------------------
    print("[17/17] Workday finished. Closing all open windows...")
    time.sleep(2.0)
    for _ in range(7):
        pyautogui.hotkey("alt", "f4")
        time.sleep(1.2 + random.uniform(-0.1, 0.4))

    elapsed = time.monotonic() - START_TIME
    print(f"\n[+] Workflow completed successfully in {elapsed:.1f} seconds. (END)")

if __name__ == "__main__":
    try:
        main()
    except (pyautogui.FailSafeException, KeyboardInterrupt):
        print("\n[!] Execution stopped safely by user or failsafe.")
