# Verify there are no unstaged/untracked files under altium/.
import re
import subprocess
import argparse

status = subprocess.check_output("git status --porcelain", encoding="utf8")
pattern = re.compile("^.(.) (.*)$")
for line in status.splitlines():
	match = pattern.match(line)
	if match.group(1) != " ":
		if match.group(2).startswith("altium/"):
			raise UserWarning("Unstaged or untracked file on altium/ path.")

parser = argparse.ArgumentParser()
parser.add_argument("proj", nargs="?", default=None, help="choose: dcdc, clk")
args = parser.parse_args()

# 1. Run all Altium output job containers.
# 2. Format the bill of materials spreadsheet.
if args.proj is None or args.proj == "dcdc":
	import altium.DCDC_CHANNEL.job.run_all_containers
	import altium.DCDC_CHANNEL.bom.format_bom
if args.proj is None or args.proj == "clk":
	import altium.CLK_DISTRO.job.run_all_containers
	import altium.CLK_DISTRO.bom.format_bom
