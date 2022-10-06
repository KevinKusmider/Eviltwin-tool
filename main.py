import os
import sys

sys.path.append('/home/kusmider/scriptMerge/src/')

import settings
from functions import *
from csv import reader
from simple_term_menu import TerminalMenu
from tabulate import tabulate

ssid = "ssid TEST"
interfaceAP = None
interfaceInternet = None
interfaceDeauth = None


def main():
	loop = True
	settings.init()
	while loop:
		loop = displayMenu()

if __name__ == "__main__":
    main()
