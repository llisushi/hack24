# hack24
NTU x ST Engineering : hack24
# Annual Dinner 2026 Planning & Budget Agent

An autonomous desktop agent simulating realistic, human-paced corporate office workflows across Windows applications. The agent drafts an event proposal in WPS Writer, processes incoming priority emails, performs budget balance analysis in WPS Spreadsheets, researches eligible lucky draw prizes across web storefronts, and finalizes internal proposal documentation.

---

## 🛠️ Environment & Prerequisites

- **Operating System:** Windows 10 or Windows 11
- **Python Version:** Python 3.10 or higher
- **Applications Required:**
  - [Google Chrome](https://www.google.com/chrome/) (registered in standard system paths)
  - [WPS Office Suite](https://www.wps.com/) (WPS Writer & WPS Spreadsheets)

---

## 🖥️ Evaluation Environment & Execution Instructions

The agent is pre-configured and ready to run inside our allocated evaluation VM.

### 1. Access the VM
- **Node:** `pve-03`
- **VM ID / Name:** `3241 (vm-team24-user1)`
- Open the console and log into the Windows desktop environment.

---

### 2. Pre-Configured Files & File Locations

All required scripts, calibration data, and target documents are already set up inside the VM:

- **Script & Calibration Files (`Downloads` folder):**
  - `merge ver 2.0.py` (Main agent script)
  - `wps_click_positions.json` (Pre-calibrated WPS toolbar coordinates)
  - `budget_click_positions.json` (Pre-calibrated budget UI coordinates)
  - *Path:* `C:\Users\<User>\Downloads\`

- **Target Budget Spreadsheet (`Desktop`):**
  - `Budget List for Annual Dinner (draft)` (`.xlsx`, `.xls`, `.xlsm`, `.et`, or `.csv`)
  - *Path:* `C:\Users\<User>\Desktop\`

> **Note:** The script will automatically generate the local workspace folder (`Desktop/AnnualDinner2026/`) and required email/web simulation templates on initial execution.

---

### 3. How to Run the Agent

1. Open the **`Downloads`** folder in File Explorer.
2. Double-click **`merge ver 2.0.py`** (it will open directly in **Python IDLE**).
3. In the IDLE window, press **`F5`** on your keyboard (or click **Run** → **Run Module** in the top menu).
4. **Hands-Off Execution:** 
   Once the script begins running, leave the mouse and keyboard untouched. The agent will autonomously execute the entire simulated workflow (~15 minutes) across WPS Writer, Outlook/Chrome, File Explorer, and WPS Spreadsheets.

> **Emergency Stop / Fail-Safe:** If you need to stop the automation early, forcefully slam the mouse cursor into any of the screen's four outer corners to trigger PyAutoGUI's built-in fail-safe.
