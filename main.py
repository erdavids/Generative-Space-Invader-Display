import random
import time
import board
import neopixel

# Lambdas for picking random RGBs
r = lambda: random.randint(0,200)

# Dimensions of the 7x7 array
width = 7
height = 7

# Time between transitions
transTime = 10
transStepTime = 0

# Single list
finalList = []

# Normalized array for creating the single list
# Holds references for the y value in our arrays
normalPixel = []
for row in range(0, height):
    normalPixel.append([])
    for col in range(0, width):
        normalPixel[row].append(0)
elementIterator = 0
for row in range(0, height):
    for col in range(0, width):
        if (row%2 == 0):
            normalPixel[row][col] = elementIterator
        else:
            normalPixel[row][width - col - 1] = elementIterator
        elementIterator += 1

# Create empty final list
for col in range(0, width*height):
    finalList.append((0,0,0))


# Instantiate neopixels and fill board
pixels = neopixel.NeoPixel(board.D4, 49, brightness=.2, auto_write=False)
pixels.fill((0,0,0))
pixels.write()

# Create and return random RGB value
def makeColor():
    red = r()
    blue = r()
    green = r()
    rgb = [red, blue, green]
    
    chance = random.randint(0, 2)
    rgb[chance] = 0
    
    return (rgb[0], rgb[1], rgb[2])

# Returns a tuple of 3 random RGBs and 3 'emptys' to simulate pixel color chance (50%)
def pickColors():
    return (makeColor(), makeColor(), makeColor(), (0,0,0),(0,0,0),(0,0,0))

# Creates, colors, and returns array
def colorArray():
    list = []
    for row in range(0, height):
        list.append([])
        for col in range(0, width):
            list[row].append((0,0,0))
    randColors = pickColors()
    for row in range(0, height):
        # index 0 and 6
        zeroSix = random.choice(randColors)
        # index 1 and 5
        oneFive = random.choice(randColors)
        # index 2 and 4
        twoFour = random.choice(randColors)
        # index 3
        three = random.choice(randColors)
        # Add the colors to the array
        list[row][0] = zeroSix
        list[row][1] = oneFive
        list[row][2] = twoFour
        list[row][3] = three
        list[row][4] = twoFour
        list[row][5] = oneFive
        list[row][6] = zeroSix
    return list
    
# Converts the array into a single normalized list using our normalized array
def convertToSingleList(list):
    counter = 0
    for row in range(0, height):
        for col in range(0, width):
            finalList[normalPixel[row][counter]] = list[row][col]
            counter += 1
        counter = 0


#############
# TRANSITIONS
#############

def replaceFromBottom(oldList, newList):
    for i in range(0, height):
        for col in range(0, height - 1):
            oldList[col] = oldList[col + 1]
        oldList[height-1] = newList[i]
        outputToDisplay(oldList)
        time.sleep(transStepTime)


def replaceFromTop(oldList, newList):
    for i in range(0, height):
        for col in range(0, height - 1):
            oldList[height - 1 - col] = oldList[height - 2 - col]
        oldList[0] = newList[height - 1 - i]
        outputToDisplay(oldList)
        time.sleep(transStepTime)


def replaceFromRight(oldList, newList):
    for col in range(0, width):
        for row in range(0, height):
            for j in range(0, width-1):
                oldList[row][j] = oldList[row][j+1]
            oldList[row][width - 1] = newList[row][0+col]
        outputToDisplay(oldList)
        time.sleep(transStepTime)


def replaceFromLeft(oldList, newList):
    for col in range(0, width):
        for row in range(0, height):
            for j in range(0, width - 1):
                oldList[row][width - 1 - j] = oldList[row][width - 2 - j]
            oldList[row][0] = newList[row][width - 1 - col]
        outputToDisplay(oldList)
        time.sleep(transStepTime)

########
# OUTPUT
########

def outputToDisplay(list):
    convertToSingleList(list)
    for col in range(0, len(finalList)):
        pixels[col] = finalList[col]
    pixels.write()



#######
# START
#######

# Create the initial array
currentArray = colorArray()

# Loop forever
while True:
    # Change the random seed based on time
    startTime = time.monotonic()
    random.seed(int(startTime * 1000))
    
    # Create the next array and display the current one
    nextArray = colorArray()
    outputToDisplay(currentArray)
    time.sleep(transTime)
    
    # Choose a random transition
    chance = random.randint(0, 3)
    if (chance == 0):
        replaceFromTop(currentArray, nextArray)
    elif (chance == 1):
        replaceFromBottom(currentArray, nextArray)
    elif (chance == 2):
        replaceFromLeft(currentArray, nextArray)
    else:
        replaceFromRight(currentArray, nextArray)
    time.sleep(transTime)
