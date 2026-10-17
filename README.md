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

All required scripts, calibration coordinates, and target budget documents are already placed in their required directories inside the VM:

- **Script & Coordinate Configuration (`Downloads\FINAL\`):**
  - `agent.py` *(Main execution script)*
  - `wps_click_positions.json` *(Pre-calibrated toolbar button coordinates)*
  - `budget_click_positions.json` *(Pre-calibrated UI navigation coordinates)*
  - *Full Path:* `C:\Users\<User>\Downloads\FINAL\`

- **Target Budget Spreadsheet (`Desktop`):**
  - `Budget List for Annual Dinner (draft)` (`.xlsx`, `.xls`, `.xlsm`, `.et`, or `.csv`)
  - *Full Path:* `C:\Users\<User>\Desktop\`

> **Note:** The script will automatically generate the local workspace folder (`Desktop/AnnualDinner2026/`) and required email/web simulation templates on initial execution.


