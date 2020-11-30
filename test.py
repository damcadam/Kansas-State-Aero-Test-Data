import os  # required for os.system(“cls”)
import csv  # required to process csv file.
import time  # required for time functions
import datetime as dt
import matplotlib.pyplot as plt  # required for plotting
import numpy as np  # required to convert to numerical array
from connector import OBDConnector  # required to include OBDConnector class
from os import system, name
from time import sleep

# define our clear function


def screen_clear():
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# define the main menu
def MainMenu():
    os.system("cls")
    screen_clear()
    print("1.  Query PID Data")
    print("2.  Graph PID Data")
    print("3.  Show Test Data")
    print("4.  Exit Program")
    selection = input("Input your selection...")
    return selection

# define screen 1


def screen1():
    #
    # Create menu listing of PIDS based on
    # contents of piddata.csv.  Disable options
    # that are not enabled for connected
    # vehicle.  Display PID data for option
    # selected by user.
    #
    # # Clearing the Screen
    screen_clear()

    # # Request disabled data for 1st 128 PIDs
    str1 = e.getPIDsingle("PIDE")

    # # Setting loop
    i = 0

    # # Read the csv file and output only the enabled PIDs
    with open('piddata2.csv', mode='r') as csv_file1:
        csv_reader1 = csv.DictReader(csv_file1)
        for row in csv_reader1:
            if (row["PID"] == "0100" or row["PID"] == "0120" or row["PID"] == "0140" or row["PID"] == "0160"):
                continue
            elif (str1[i] == "1"):
                print(f'{row["PID"]} - {row["Description"]} ({row["Units"]})')
            i = i+1
    # # Input PID
    PID = input("Select PID From List ")

    # # Output PID value with units
    with open('piddata2.csv', mode='r') as csv_file2:
        csv_reader2 = csv.DictReader(csv_file2)
        for row in csv_reader2:
            if (row["PID"] == PID):
                num = str(e.getPIDsingle(PID))
                print("PID DATA FOR " + PID + " = " +
                      num + " " + f'{row["Units"]}')

    # # Pause system
    print("Press any key to return to the main menu")
    os.system("PAUSE >nul")
    screen_clear()

# define screen 2


def screen2():
    #
    # Create menu listing of PIDS based on
    # contents of piddata.csv.  Disable options
    # that are not enabled for connected
    # vehicle.  Plot PID data for option
    # selected by user.
    #

    # Clearing the Screen
    screen_clear()

    # # Request PID data
    str1 = e.getPIDsingle("PIDE")
    str2 = e.getPIDsingle("PIDN")
    print(str1)
    print(str2)

    # # Combine PID data
    str3 = ''
    i = 0
    while(i < len(str1)):
        if(str1[i] == '1' and str2[i] == '1'):
            str3 = str3 + '1'
        else:
            str3 = str3 + '0'
        i = i+1
    print(str3)

    # # Setting loop
    i = 0

    # # Read the csv file and output only the enabled PIDs
    with open('piddata2.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if (row["PID"] == "0100" or row["PID"] == "0120" or row["PID"] == "0140" or row["PID"] == "0160"):
                continue
            elif (str3[i] == "1"):
                print(f'{row["PID"]} - {row["Description"]} ({row["Units"]})')
            i = i+1

    # # Input PID
    PID = input("Select PID From List ")

    i = 0
    # # Output PID value with units
    with open('piddata2.csv', mode='r') as csv_file2:
        csv_reader2 = csv.DictReader(csv_file2)
        for row in csv_reader2:
            if (row["PID"] == PID):
                tdat, pdat = e.getPIDmultiple(PID, 1, 1000) ############################## Change Back to 60 before submit
                tdat = np.array(tdat, dtype=np.float32)
                pdat = np.array(pdat, dtype=np.float32)
                fig = plt.figure()
                plt.title("PID DATA FOR " + PID)
                plt.xlabel("time (ms)")
                plt.ylabel("PID DATA ({})".format(row["Units"]))
                plt.scatter(tdat, pdat, marker='o', label='pid data')
                plt.legend(loc='upper left')
                plt.grid(True)
                plt.show()
            i = i + 1

    if plt.fignum_exists(fig):
        os.system("PAUSE >nul")
    else:
        screen_clear()
        return

# define screen 3


def screen3():
    # # Clearing the screen
    screen_clear()

    # # Calling for Tests PID and removing spaces from return
    str1 = e.getPIDsingle("0141")
    str2 = ''
    i = 0
    while(i < len(str1)):
        if(str1[i] != ' '):
            str2 = str2 + str1[i]
        i = i+1

    # # Looking for Bit 0
    i = 0
    k = 0
    while (i < len(str2)):
        k = k + 1
        if(str2[i] == '0' and str2[i+1] == '0'):
            k = k - 1
            break
        i = i+1
    str3 = ''

    # # Excluding everything before Bit 0
    while (k < len(str2)):
        str3 = str3 + str2[k]
        k = k+1
    
    # # Converting to Binary
    bin1 = "0" + bin(int('1'+ str3, 16))[3:]

    # Convert bin1 to list
    bin2 = []
    bin2[:0]=bin1

    # Find and replace
    i = 0
    while (i < len(bin1)):
        # Changing B byte to e/d
        if (i >= 8 and i <= 11):
            if (bin2[i] == '0'):
                bin2[i] = "disabled"
            elif (bin2[i] == '1'):
                bin2[i] = "enabled"
        # Changing B byte to c/i
        elif (i >= 12 and i <= 15):
            if (bin2[i] == '0'):
                bin2[i] = "incomplete"
            elif (bin2[i] == '1'):
                bin2[i] = "complete"
        # Changing C byte to e/d
        elif (i >= 16 and i <= 23):
            if (bin2[i] == '0'):
                bin2[i] = "disabled"
            elif (bin2[i] == '1'):
                bin2[i] = "enabled"
        # Changing D byte to c/i
        elif (i >= 24 and i <= 32):
            if (bin2[i] == '0'):
                bin2[i] = "incomplete"
            elif (bin2[i] == '1'):
                bin2[i] = "complete"
        i += 1
    
    # # Defining Names
    types = ["Misfire ","Fuel System ","Components", "Catalyst ","Heated Catalyst ","Evaporative System ","Secondary Air System ",
            "A/C Refrigerant ","Oxygen Sensor ","Oxygen Sensor Heater ","EGR System "]
    
    # # Printing Output
    i = 0
    while (i < len(types)):
        if (i == 0 or i == 1 or i == 2):
            print("{} ({},{})".format(types[i],bin2[i+9],bin2[i+13])) 
        else:
            print("{} ({},{})".format(types[i],bin2[i+14],bin2[i+22]))
        i += 1

    print("Press any key to return to the main menu")
    os.system("PAUSE >nul")
    screen_clear()


#
#   Begin main program
#
# Create instance of the OBDConnector object.
# Set verbosity to False to suppress debug printing
e = OBDConnector(False)
# Connect to the Arduino
e.connect()
# Initialize the main menu selection.
selection = 0
# Loop until user selects to exit
while (selection != "4"):
    # Display main menu and store user
    # selection.
    selection = MainMenu()
    # Branch based on user selection.
    if (selection == "1"):
        screen1()
    elif (selection == "2"):
        screen2()
    elif (selection == "3"):
        screen3()

# Clear the screen
screen_clear()
# Close the OBDConnector object
e.close()
