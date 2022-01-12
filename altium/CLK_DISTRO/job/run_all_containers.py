import glob
import os
import time

import psutil
from pywinauto.application import Application

# Start Altium Designer or connect to it if already open.
exe_name = "X2.EXE"
exe_path = "C:/Program Files/Altium/AD22/"

if exe_name in (p.name() for p in psutil.process_iter()):
    app = Application().connect(path=exe_path + exe_name)
    cleanup = False
else:
    app = Application().start(exe_path + exe_name)
    time.sleep(15)
    cleanup = True

# Open the job file. Close once in case already open.
job_path = os.path.dirname(__file__)
job_file = glob.glob(job_path + "/*.OutJob")[0]

top_dlg = app.window(title_re=".*Altium Designer.*")

for i in range(2):
    time.sleep(1)
    top_dlg.type_keys("^o")
    time.sleep(1)
    open_dlg = app.window(title_re=".*Choose Document to Open.*")
    open_dlg.type_keys(job_file)
    open_dlg.Open.click()
    time.sleep(4)
    if not i:
        top_dlg.type_keys("^{F4}")

# Tab over to output containers. For each container, run output with F9.
top_dlg.type_keys("{TAB}")
job_count = 2
for i in range(job_count):
    time.sleep(1)
    top_dlg.type_keys("{UP}")

for i in range(job_count):
    time.sleep(1)
    top_dlg.type_keys("{F9}")
    time.sleep(2)
    top_dlg.type_keys("{DOWN}")

# Cleanup.
time.sleep(1)
top_dlg.type_keys("^{F4}")
time.sleep(1)
if cleanup:
    top_dlg.type_keys("%{F4}")
