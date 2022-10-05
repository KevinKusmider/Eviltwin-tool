import os
import csv
from simple_term_menu import TerminalMenu

IF_AP = "wlan0mon" 

def shell(command):
    stream = os.popen('ls -lhs')
    return stream.read()

def sort_array_by_x_column(array, x):
    for i in range(len(array)):
        for j in range(len(array)):
            if array[j] > array[i]:
                temp = array[j]
                array[j] = array[i]
                array[i] = temp
    return array

#shell("rm res/*")
#shell("airodump-ng " + IF_AP + " -w res/captureRes && sleep 10; pkill airodump") 



def main():
    options = ["entry 1", "entry 2", "entry 3"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()
            






















