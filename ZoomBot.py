import webbrowser           #no pip needed
import time                 #no pip needed
import pyautogui as pygui   #pip install needed
import os                   #literally only need this for one thing

pygui.PAUSE = 0.25
pygui.FAILSAFE = True

class ZoomBot():
    def __init__(this, link="", timeTillJoin=0, timeTillEnd=0):
        this.link = link
        this.timeTillJoin = timeTillJoin
        this.timeTillEnd = timeTillEnd
        this.enteredCall = False
        this.inCall = False
        this.leftCall = False
    #accessors
    def getTimeTillJoin(this):
        return this.timeTillJoin
    def getTimeTillEnd(this):
        return this.timeTillEnd
    def getLink(this):
        return this.link
    #mutators
    def setTimeTillJoin(this, timeTillJoin):
        this.timeTillJoin = timeTillJoin
    def setTimeTillEnd(this, timeTillEnd):
        this.timeTillEnd = timeTillEnd
    def setLink(this, link):
        this.link = link
    #checks the time to see if it is past login/logout time
    def checkTime(this, time):
        if time >= this.timeTillEnd and this.inCall and this.enteredCall:
            this.logout()
        if time >= this.timeTillJoin and not this.enteredCall:
            this.login()
    #logs in to the Zoom session
    def login(this):
        webbrowser.open(this.link)
        this.enteredCall = True
        this.inCall = True
    #logs out of the Zoom session
    def logout(this, buttonImg=(os.getcwd()+"\\buttons\\zoom_leave_meeting.png")):
        pygui.hotkey('altleft','q')
        time.sleep(1)
        pygui.click(pygui.center(pygui.locateOnScreen(buttonImg)))
        this.inCall = False
        this.leftCall = True
    #resets all the flags in order to do another call
    def resetFlags(this):
        this.inCall = False
        this.enteredCall = False
        this.leftCall = False
    
        
