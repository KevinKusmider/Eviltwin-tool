import os
import sys
import json
from csv import reader
from simple_term_menu import TerminalMenu
from tabulate import tabulate

with open("conf/local.json") as json_data_file:
	data = json.load(json_data_file)

sys.path.append(data["pathSRC"])

import settings
from functions import *


def main():
	loop = True
	settings.init()
	while loop:
		loop = displayMenu()

if __name__ == "__main__":
    main()
