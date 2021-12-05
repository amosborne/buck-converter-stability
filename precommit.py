# Verify there are no unstaged/untracked files under altium/.
import re
import subprocess

status = subprocess.check_output("git status --porcelain", encoding="utf8")
pattern = re.compile("^.(.) (.*)$")
for line in status.splitlines():
	match = pattern.match(line)
	if match.group(1) != " ":
		if match.group(2).startswith("altium/"):
			raise UserWarning("Unstaged or untracked file on altium/ path.")

# Run all Altium output job containers.
import altium.job.run_all_containers

# Format the bill of materials spreadsheet.
import altium.bom.format_bom
