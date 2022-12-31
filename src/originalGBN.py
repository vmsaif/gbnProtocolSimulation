
__author__ = "Saif Mahmud"
__purpose__ = "Implementing original GO-Back-N protocol simulation"
__version__ = "1.0"
__dateCreated__ = "2022-11-24 18:42:25"

import random
import matplotlib.pyplot as plt
import json

# constants
NUMBER_OF_SIMULATIONS = 500
WINDOW_SIZE = 4

global cumulativeAttemptsArrQ2
cumulativeAttemptsArrQ2 = []

global cumulativeAttempts
cumulativeAttempts = 0

class MyPacket:
    def __init__(self, id):
        self.id = id

    def ackRecieved(self):
        randomNum = random.randint(1, 100)
        if(randomNum <= 35):
            return False
        else:
            return True

    def __str__(self):
        return str(self.id)

class MyWindow:
    def __init__(self, size):
        self.size = size
        self.packets = []

    def addPacket(self, packet):
        self.packets.append(packet)

    def __str__(self):
        return str(self.packets)

    def windowSent(self):
        global cumulativeAttempts
        global cumulativeAttemptsArrQ2

        out = True;
        
        for i in range(0, len(self.packets)):
            print("Attempting to send packet of index " + str(self.packets[i].id))
            
            if(self.packets[i].ackRecieved() == False):
                out = False
                print("--! Packet Acknowledgement of packet " + str(self.packets[i].id) + " was not recieved.")
            else:
                cumulativeAttempts += 1
        cumulativeAttemptsArrQ2.append(cumulativeAttempts)
        return out


def main():
    
    allPackets = []
    for i in range(WINDOW_SIZE * NUMBER_OF_SIMULATIONS * 2):
        allPackets.append(MyPacket(i)) 

    startSimulation(allPackets)
    
    # ------------graph part ----------------
    
    # uncomment to see the graph
    drawQ2Graph()
    
    # -------------------------------------

def drawQ2Graph():
    q1file = open("modifiedGBN.json")
    cumulativeAttemptsArrQ1 = json.loads(q1file.read())
    plt.plot(attempts, cumulativeAttemptsArrQ1, label = "Modified Go-Back-N")
    plt.plot(attempts, cumulativeAttemptsArrQ2, label = "Original Go-Back-N")

    # naming the x axis
    plt.xlabel('Window Size')
    # naming the y axis
    plt.ylabel('Attempts')

    # giving a title to my graph
    plt.title('Cumulative total number of frames sent by the modified GBN and original GBN algorithms')

    # show a legend on the plot
    plt.legend()    
    
    # function to show the plot
    plt.show()

def startSimulation(myPackets):
    global windowSizes #for the graph
    global attempts #for the graph

    windowSizes = []
    attempts = []
    
    i = 0
    currIndex = 0
    
    while (i <= NUMBER_OF_SIMULATIONS and currIndex < len(myPackets)):
        windowSizes.append(WINDOW_SIZE)
        attempts.append(i+1)
        aWindow = MyWindow(WINDOW_SIZE)
        print("Simulation: "+ str(i) + "\nWindow Size is: " + str(WINDOW_SIZE))
        for j in range(currIndex, currIndex + int(WINDOW_SIZE)):
            if currIndex + int(WINDOW_SIZE) < len(myPackets):
                aWindow.addPacket(myPackets[j])

        temp = aWindow.windowSent()
        if(temp == True): 
            # increase WindowSize by 1
            currIndex = currIndex + WINDOW_SIZE
            print("The window frame was sent successfully.")
            
        print()
        i = i + 1

if __name__ == "__main__":
    main()  # call main function


