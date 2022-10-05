import os
import sys
from functions import *
from csv import reader
import numpy
from simple_term_menu import TerminalMenu
sys.path.append('/home/kali/Desktop/ScriptTP/functions')

IF_AP = "wlan1"
ssid = "ssid TEST"
interfaceAP = None
interfaceInternet = None
interfaceDeauth = None

#shell("rm res/*")

def main():
	while True:
		displayMenu(interfaceAP, interfaceInternet, interfaceDeauth)

if __name__ == "__main__":
    main()
