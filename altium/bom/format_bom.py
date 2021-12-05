import glob
import os
import time

import psutil
from pywinauto.application import Application

# Start LibreOffice Calc or connect to it if already open.
exe_name = "scalc.exe"
exe_path = "C:/Program Files/LibreOffice/program/"

if not exe_name in (p.name() for p in psutil.process_iter()):
    Application().start(exe_path + exe_name, wait_for_idle=False)
    time.sleep(5)

app = Application().connect(title_re=".*LibreOffice Calc.*")

# Open the bom file. Close once in case already open.
bom_path = os.path.dirname(__file__)
bom_file = glob.glob(bom_path + "/*.xlsx")[0]

top_dlg = app.top_window()

time.sleep(1)
top_dlg.type_keys("^o")
time.sleep(1)
open_dlg = app.window(title_re=".*Open.*")
open_dlg.type_keys(bom_file)
open_dlg.Open.click()
time.sleep(4)

# Auto-filter and auto-column-width.
top_dlg.type_keys("^a")
top_dlg.type_keys("%d%f{ENTER}")
top_dlg.type_keys("%o%m%o{ENTER}")

# Delete extra sheets.
for i in range(2):
    top_dlg.type_keys("^{TAB}")
    top_dlg.type_keys("%s%d{ENTER}")

# Exit.
top_dlg.type_keys("^s")
time.sleep(2)
top_dlg.type_keys("^q")
