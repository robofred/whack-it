####################################################################################
#######################     RAPTOR - Testing Firmware       ########################
#######################     Maybrook Partners LLC - 2021    ########################
#######################     Commercial Software - All Rights Reserved   ############
#######################     Author: Fred Nikgohar           ########################
#######################     Contact: frednikgohar@gmail.com    #####################
####################################################################################



####################################################################################
##############################      PYTHON IMPORTS     #############################
####################################################################################


from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from digitalio import DigitalInOut, Direction, Pull

import board
import adafruit_dotstar as dotstar

import time
import random
from array import array

from raptorBleName import deviceID, deviceName, deviceList, moleSleep


####################################################################################
#############################      DEVICE CONSTANTS     ############################
####################################################################################

# On-board DotStar for boards including Gemma, Trinket, and ItsyBitsy
dots = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5)
# For Gemma M0, Trinket M0, Metro M0 Express, ItsyBitsy M0 Express, Itsy M4 Express, QT Py M0
switch = DigitalInOut(board.D2)
# switch = DigitalInOut(board.D5)  # For Feather M0 Express, Feather M4 Express
# switch = DigitalInOut(board.D7)  # For Circuit Playground Express
switch.direction = Direction.INPUT
switch.pull = Pull.UP


# LED setup.
led = DigitalInOut(board.LED)
# For QT Py M0. QT Py M0 does not have a D13 LED, so you can connect an external LED instead.
# led = DigitalInOut(board.SCK)
led.direction = Direction.OUTPUT



ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)


####################################################################################
#############################      SIMPLE GAME CODE     ############################
####################################################################################


# 1 - Generate a Random list of devices from 1 to 5, each coresponding to Device ID (universal list for all devices)
# 2 - Each device to generate a random number coresponding to each item in List above
# 3 - If List2 is even (mole) odd (no mole)
# 4 - All devices get a simultaneous start, and all mole/no-mole are constant time, therefore
# 5 - As each devic loops through List1, check to see mole, record btn push and/or turn off based on constant time
# 6 - When List1 finished, publish results

moleList = []                  # to assign odd/even random numbers to each deviceID in dList
dListNum = len(deviceList)     # how many devices in deviceList?




def LightsOff():
    dots[0] = (0,0,0)



def ResetGame():
    for x in range(dListNum):      # populate array with odd/even numbers for mole/no-mole
        # print(deviceList[x])
        moleID = random.randint(1,100)
        moleList.append(moleID)
        # print("Assigned: " + str(moleID))
        x +=1
    LightsOff()
    print("**********************************************")
    print("*************  GAME WAS RESET  ***************")
    print("**********************************************")




def SimpleGame():
    ResetGame()
    for x in range(dListNum):
        if (str(deviceList[x]) == str(deviceID)):
            if (moleList[x] % 2 == 0):
                print("Mole")
                dots[0] = (255,0,0)
                time.sleep(moleSleep)
            else:
                print("No Mole")
                dots[0] = (0,255,0)
                time.sleep(moleSleep)
        else:
            print("I'm OFFFFFFF")
            dots[0] = (0,0,0)
            time.sleep(moleSleep)
    print("DONE!")




while True:
    ble.start_advertising(advertisement)
    led.value = False
    print("Waiting to connect")
    while not ble.connected:
        pass
    ble.name = deviceName
    print("Connected")

    while ble.connected:
        s = uart.readline().decode("utf-8")
        if s:
            SimpleGame()
            # myUart = s.split(",", 1)
            # gameBlink = int(myUart[0])
            # gameTime = float(myUart[1])
            # PatternGame(gameBlink, gameTime)
            LightsOff()
            uart.write("Done")