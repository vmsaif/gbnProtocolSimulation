
__author__ = "Saif Mahmud"
__purpose__ = "Implementing a modified GO-Back-N protocol simulation"
__version__ = "1.0"
__dateCreated__ = "2022-11-22 18:42:25"

import random
import matplotlib.pyplot as plt
import json
# constants
NUMBER_OF_SIMULATIONS = 500
MINIMUM_WINDOW_SIZE = 1
MAXIMUM_WINDOW_SIZE = 8

global windowSizes #for the graph
global attempts #for the graph

global cumulativeAttempts
global cumulativeAttemptsArrQ1
cumulativeAttempts = 0
cumulativeAttemptsArrQ1 = []

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
        global cumulativeAttemptsArrQ1
        
        out = -1;
        
        for i in range(0, len(self.packets)):
            print("Attempting to send packet of index " + str(self.packets[i].id))
            
            if(self.packets[i].ackRecieved() == False):
                out = self.packets[i].id
                print("--! Packet Acknowledgement of packet " + str(self.packets[i].id) + " was not recieved.")
            else:
                cumulativeAttempts += 1
        cumulativeAttemptsArrQ1.append(cumulativeAttempts)
        return out


def main():
    
    allPackets = []
    for i in range(MAXIMUM_WINDOW_SIZE * NUMBER_OF_SIMULATIONS * 2):
        allPackets.append(MyPacket(i))

    startSimulation(allPackets)
    
    # ------------graph part----------------
    
    # uncomment to see the graph
    creatingJsonFileForQ2Graph()
    drawQ1Graph()
    
    # -------------------------------------

def creatingJsonFileForQ2Graph():
    saveValue = open("modifiedGBN.json", "w")
    saveValue.write(json.dumps(cumulativeAttemptsArrQ1))
    saveValue.close()

def drawQ1Graph():
    plt.plot(attempts, windowSizes)
  
    # naming the x axis
    plt.xlabel('Window Size')
    # naming the y axis
    plt.ylabel('Attempts')

    # giving a title to my graph
    plt.title('Window Sizes versus the number of Sending Attempts')

    # function to show the plot
    plt.show()

def startSimulation(myPackets):
    global windowSizes #for the graph
    global attempts #for the graph

    windowSizes = []
    attempts = []

    currentWindowSize = 4 # initial window size
    
    i = 0
    currIndex = 0
    
    while (i <= NUMBER_OF_SIMULATIONS and currIndex < len(myPackets)):
        windowSizes.append(currentWindowSize)
        attempts.append(i+1)
        aWindow = MyWindow(currentWindowSize)
        print("Simulation: "+ str(i) + "\nCurrent Window Size is: " + str(currentWindowSize))
        for j in range(currIndex, currIndex + int(currentWindowSize)):
            if currIndex + int(currentWindowSize) < len(myPackets):
                aWindow.addPacket(myPackets[j])

        temp = aWindow.windowSent()
        if(temp == -1): #true
            # increase WindowSize by 1
            currIndex = currIndex + currentWindowSize
            currentWindowSize = currentWindowSize + 1

            if(currentWindowSize >= MAXIMUM_WINDOW_SIZE):
                currentWindowSize = MAXIMUM_WINDOW_SIZE
            else:
                print("The window frame was sent successfully.")
                print("--> Increasing Window Size by 1")
            
        else: #false
            # decrease WindowSize by half
            currentWindowSize = int(currentWindowSize / 2)
            if(currentWindowSize < MINIMUM_WINDOW_SIZE):
                currentWindowSize = MINIMUM_WINDOW_SIZE
            else:
                print("--> Decreasing Window Size by half")
            currIndex = temp  
            
        print()
        i = i + 1

if __name__ == "__main__":
    main()  # call main function


