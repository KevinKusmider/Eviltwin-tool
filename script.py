import os
import csv
import numpy as np
from simple_term_menu import TerminalMenu
from tabulate import tabulate

IF_AP = "wlan0mon" 
CAPTURE_TIME = "10" 

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

def print_array(array):
    for row in array:
        print(row)

def get_aps():
    accessPoints = {"header" : [], "aps" : []}
    with open("res/captures-01.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            accessPoints["aps"].append(row)
             
    # Set header, and remove it from aps array
    accessPoints["aps"].pop(0)
    #maxDisplayChar = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    #for index, column in enumerate(accessPoints["aps"][0]):
        #accessPoints["header"].append([column, maxDisplayChar[index]])
    accessPoints["headers"] = accessPoints["aps"][0]    
    accessPoints["aps"].pop(0)

    # Remove second part of aps infos
    index = None 
    for i, ap in enumerate(accessPoints["aps"]):
        if not ap:
            index = i
            break

    del accessPoints["aps"][index:]

    return accessPoints



def main():
    print("airmon-ng start " + IF_AP)
    print(shell("airmon-ng start " + IF_AP))

    #shell("rm res/*")
    #shell("airodump-ng " + IF_AP + " -w res/captures && sleep " + CAPTURE_TIME + " ; pkill airodump") 

    aps = get_aps();
    print(tabulate(aps["aps"], aps["headers"], tablefmt="pretty"))

if __name__ == "__main__":
    main()
            






















