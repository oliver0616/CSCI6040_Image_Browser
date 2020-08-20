# Course: CSCI 6040
# Group Members: Huan-Yun Chen, Ethen Smith, Mostafa Namian
# Project: Image Browser with openCV

import os
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import sys

'''
args for command line
'''
args = sys.argv[1:]

if args[0] == "-h" or args[0] == "--help" or args[0] == "--?":
    print("print this message")
    exit()
elif args[0] == "run":
    print("program started")
elif args[0] == "--cols" or args[0] == "--c":
    print("number of cols")
    exit()
elif args[0] == "--rows" or args[0] == "--r":
    print("number of rows")
    exit()
elif args[0] == "directory" or args[0] == "--d":
    print("/testImages")
    exit()
else :
    print("no args")
    exit()




'''
This function allow user to select a directory and display all the image file in the directory textbox
'''



def selectDirectory():
    global firstFlag
    global filePathList

    # Remove all items within listbox and assign new items
    if not firstFlag:
        listboxPane.delete(0, END)
        filePathList = []
    # Get directory files
    dirPath = filedialog.askdirectory()
    # TODO get all jpeg file here
    if not dirPath == "":
        for name in os.listdir(dirPath):
            listboxPane.insert('end', name)
            currentFilePath = os.path.join(dirPath, name)
            filePathList.append(currentFilePath)
        firstFlag = False


'''
This function display the selected image
'''
def displayImage(imagePath):
    global imagePanel

    # TODO collect meta data function here
    # Read the image and convert to tkinter image, resize image if image is bigger than require scale
    image = cv2.imread(imagePath)
    resizeWidth, resizeHeight = calResizePercentage(image.shape[1], image.shape[0])
    if not resizeWidth == 0 and not resizeHeight == 0:
        image = cv2.resize(image, (resizeWidth, resizeHeight), interpolation = cv2.INTER_AREA)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    # Update image panel
    imagePanel.configure(image=image)
    imagePanel.image = image


'''
This function calculate the resize dimension for the image
'''
def calResizePercentage(width, height):
    global rootWidth, rootHeight, originalWidth, originalHeight

    maxWidth = rootWidth - 100
    maxHeight = rootHeight - 100
    originalWidth = width
    originalHeight = height
    widthGreaterHeight = True
    scale = 0

    if height > width:
        widthGreaterHeight = False
    if widthGreaterHeight:
        if width < maxWidth:
            return (0, 0)
        else:
            scale = maxWidth * 100 / width
    else:
        if height < maxHeight:
            return (0, 0)
        else:
            scale = maxHeight * 100 / height

    newWidth = int(width * scale / 100) 
    newHeight = int(height * scale / 100) 
    return (newWidth, newHeight)


'''
This function handle listbox item onClick event
'''
def onselect(event):
    global filePathList

    wid = event.widget
    index = int(wid.curselection()[0])
    value = wid.get(index)
    print('Selected index: %d, Selected Item: %s' % (index, value))
    displayImage(filePathList[index])


#===================================================================================================================================
# Main
firstFlag = True # Determine if the directory were first selected
filePathList = [] # List that store all image path
# Original width and height for image
originalWidth = None
originalHeight = None
rootWidth = 1000
rootHeight = 700

# initialize the window toolkit
root = Tk()
root.title( 'Image Browser' )
root.geometry("%sx%s" % (rootWidth,rootHeight)) # Window size width * height

# Directory itemlist textbox and scroll bar
listboxPane = Listbox(root)
listboxPane.pack( side = LEFT, fill=BOTH, expand=False)
listboxPane.bind('<<ListboxSelect>>', onselect)
scrollbar = Scrollbar(root)
scrollbar.pack(side = LEFT, fill=BOTH)
listboxPane.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listboxPane.yview)

# Image Panel
imagePanel = Label()
imagePanel.pack(side=TOP, padx=10, pady=10)

buttomFrame = Frame(root)
buttomFrame.pack(side=BOTTOM)
# Select directory button
dirBtn = Button(buttomFrame, text="Directory Path", command=selectDirectory)
infoBtn = Button(buttomFrame, text="Metadata")
dirBtn.pack(side="left", padx="10", pady="10")
infoBtn.pack(side="left", padx="10", pady="10")

# kick off the GUI
root.mainloop()
