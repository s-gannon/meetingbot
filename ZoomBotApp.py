import ZoomBot
import time
import pyautogui as pygui
import os
import re

def jiggle():
    pygui.moveRel(10,10)
    pygui.moveRel(-10,-10)

def timeTill(futureTime):   #gets futureTime as arr [hrs, minutes]
    ct = time.localtime()   #current time
    return (int(futureTime[0])*60*60 + int(futureTime[1])*60) - (ct[3]*60*60 + ct[4]*60)

exitFlag = False    #flag to tell program when to leave the main loop
timeNow = 0         #current time
schedule = []       #times to join and end classes; read from file
try:
    sFile = open("schedule.txt", "r")
    for line in sFile:      #splits the string into an array & appends to schedule
        if re.match("^[^;]+;[0-2]?[\d]:[0-5][\d];\d{1,};https?://[^;]+;(zoom|meets)$", line) != None:
            schedule.append(line.split(";"))
#        else:
#            print("Regex test failed. Not adding " + line + " to list")
    for line in schedule:   #replaces the newline character
        line[len(line)-1].replace("\n","")
    sFile.close()
except:
    print("File did not open correctly")
    exit()

zb = ZoomBot.ZoomBot()
print("    Welcome to the Zoom Bot Application")
while not exitFlag:
    doneFlag = False    #flag to tell the program if the Zoom call is done or not
    cls = 0     #used to number the options in the non-CS way (starting at 1)
    zb.resetFlags()
    
    print("-------------------------------------------")
    for classes in schedule:
        print(cls+1, ". ", classes[0])
        cls += 1
    print(cls+1, ".  Exit")
    inp = int(input("Enter the class number or the last option to exit: "))-1
    if inp == cls:
        exitFlag = True
    elif int(inp) < cls and int(inp) >= 0:
        clsNum = inp    #the class number (in the schedule)
        zb.setLink(schedule[clsNum][3]) #sets the link to the one listed in the schedule
        inp = input("Joining, leaving, or both?(j,l,b): ")
        if inp == "j" or inp == "b":
            zb.setTimeTillJoin(time.time() + timeTill(schedule[clsNum][1].split(":")))
        if inp == "l" or inp == "b":
            zb.setTimeTillEnd(time.time() + timeTill(schedule[clsNum][1].split(":")) + int(schedule[clsNum][2])*60)
            #zb.enteredCall = True; did not work as intended for both option
        while not doneFlag:
            if round(time.time()) % (4.25*60) <= 15:
                jiggle()
                print("Jiggling mouse...")
            zb.checkTime(time.time())
            if inp == "j" and zb.enteredCall and zb.inCall:
                doneFlag = True
            elif inp == "l" and not zb.inCall and zb.leftCall:
                doneFlag = True
            elif inp == "b" and zb.enteredCall and not zb.inCall and zb.leftCall:
                doneFlag = True
            else:
                print("Not done yet.. time to join: ", timeTill(schedule[clsNum][1].split(":")))
                print("               time to end : ", timeTill(schedule[clsNum][1].split(":")) + int(schedule[clsNum][2])*60)
            time.sleep(5);
    else:
        print("\nInput error. Number is not between 1 and ", cls+1, ".")








