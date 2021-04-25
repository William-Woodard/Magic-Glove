#nathan time imported libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import pytesseract


#lottie time imported libraries
from difflib import SequenceMatcher

#william time imported libraries
import os

def nathanTime():
    camera = PiCamera() 
    camera.resolution = (640, 480)              #Sets the camera resolution
    camera.framerate = 30                       #Sets the camera framerate
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    lines = []
    i = 0
    for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):       
        image = frame.array
        #image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        cv.imshow("Frame", image)
        key = cv.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        text = pytesseract.image_to_string(image, config='')
        print(text)
        temp = text.split("\n")
        for n in temp:
            lines.append(n)
        lines.append("##WEIRDTEXT##")
        if i > 10:
            finalText = lottieTime(lines)
            williamTime(finalText)
            i = 0
            lines = []
        else:
            pass
        i += 1
    
def lottieTime(lines):
    images = [[]] #2d list to store each images lines
    sortingList = [] #temporary list to store the lines in an image
    for x in lines:
        #adds all lines so far to a new image if ##WEIRDTEXT## is present
        if "##WEIRDTEXT##" in x:
            if(sortingList != []):
                images.append(sortingList)
                sortingList=[]
        #strips the code and adds it too the cumulative temporary list
        else:
            i = x.strip()
            if(i!=""):
                sortingList.append(i)

    #outputs text found so far

    #finds the maximum amount of lines of text in an image
    largestImage = 0
    for v in images:
        if len(v)>largestImage:
            largestImage = len(v)

    #creates a new image array with the x/y coordiantes swapped
    invertedImage = [[]]
    for y in range(largestImage):
        invertedImage.append([])
        for x in range(len(images)):
            #allows for irregular list lengths
            try:
                invertedImage[y].append(images[x][y])
            except:
                pass

    #creates array to store the data for each image,
    #which consists of an array of a similarity reading for every
    #combination of strings found in the first lines of each image
    similarities = [[[]]]
    for x in range(len(invertedImage)):
        similarities.append([])
        for y in range(len(invertedImage[x])):
            for z in range(len(invertedImage[x])):
                similarity = SequenceMatcher(None, invertedImage[x][y], invertedImage[x][z]).ratio()
                similarities[x].append([invertedImage[x][y], invertedImage[x][z], similarity])

    #adds the mode string in each position from the image to final text
    finalText=""
    for i in similarities:
        highestIndex = 0
        highestValue = 0
        p=0
        for s in i:
            try:
                if s[2]>highestValue:
                    highestIndex = p
            except:
                pass
            p+=1
        try:
            finalText+=i[highestIndex][0]+" "
        except:
            pass

    #outputs final text
    print("=======FINALTEXT=======")
    print(finalText)
    return finalText

def williamTime(finalText):
    os.system("echo '" + finalText + "' | festival --tts")


#Main
weAreCool = True
while weAreCool:
    nathanTime()
