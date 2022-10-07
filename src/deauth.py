import os
import sys
import json
import csv
from simple_term_menu import TerminalMenu
from tabulate import tabulate
from subprocess import call

with open("conf/local.json") as json_data_file:
	data = json.load(json_data_file)

sys.path.append(data["pathSRC"])
import settings

def shell(command):
	stream = os.popen(command)
	return stream.read()

def print_array(array):
	for row in array:
		print(row)

def scanDevices(wlan):
	print(shell("pwd"))
	shell("rm -f res/targetDevices/*")
	shell("airodump-ng -d " + settings.globals["bssid"] + " -c " + settings.globals["channel"] + " " + wlan + " -w res/targetDevices/captures & sleep 10; pkill airodump")

def getDevices():
	devices = {"header" : [], "devices" : []}
	with open("res/targetDevices/captures-01.csv", "r") as file:
		reader = csv.reader(file)
		for row in reader:
			devices["devices"].append(row)

	# Set header, and remove it from devices array
	devices["devices"].pop(0)
	index = None
	for i, device in enumerate(devices["devices"]):
		if not device:
			index = i
			break

	devices["devices"].pop(0)
	del devices["devices"][0:index]

	devices["header"] = devices["devices"][0]
	devices["devices"].pop(0)

	del devices["devices"][-1]

	return devices

def displaySelectDevice():
	scanDevices(settings.globals["interfaceAP"])
	devices = getDevices()
	if not devices["devices"]:
		return
	options = tabulate(devices["devices"], headers=devices["header"])
	header = options.split("\n")[0:2] 
	header = "\n".join(header)
	items = options.split("\n")[2:]
	terminal_menu = TerminalMenu(menu_entries = items, title = header)
	menu_entry_index = terminal_menu.show()
	selectedTarget = devices["devices"][menu_entry_index]
	settings.globals["deviceMAC"] = selectedTarget[0].lstrip()
