#---------------------------------------------------------------------
# Celebrity Lookalike Generator - Final Year Artefact - By Jay Devine
#---------------------------------------------------------------------

# Import necessary modules
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from PIL import ImageTk, Image
import glob
import cv2
import os
from shutil import copyfile
import sys

# Delete all Celeb Images from Reference Folder & Images from Source Folder
def emptyFolders():
    folder_path = (r'assets/representative/custom/ref/female')
    test = os.listdir(folder_path)
    for images in test:
        if images.endswith(".jpg"):
            os.remove(os.path.join(folder_path, images))
    
    folder_path2 = (r'assets/representative/custom/ref/male')
    test2 = os.listdir(folder_path2)
    for images2 in test2:
        if images2.endswith(".jpg"):
            os.remove(os.path.join(folder_path2, images2))

    folder_path3 = (r'assets/representative/custom/src/male')
    test3 = os.listdir(folder_path3)
    for images3 in test3:
        if images3.endswith(".png"):
            os.remove(os.path.join(folder_path3, images3))

    folder_path4 = (r'expr/results/custom/')
    test4 = os.listdir(folder_path4)
    for images4 in test4:
        if images4.endswith(".jpg"):
            os.remove(os.path.join(folder_path4, images4))

# Create Root Widget (Window) and Layout
root = Tk()
root.title('Celebrity Lookalike')
root.state('zoomed')
root.config(bg='cyan')

# Padding to give the GUI a better layout
padlbl = Label(root, bg='cyan')
padlbl.grid(column=0, padx=15)
padlbl1 = Label(root, bg='cyan')
padlbl1.grid(column=4, padx=15)
padlbl2 = Label(root, bg='cyan')
padlbl2.grid(column=6, padx=20)

# Creation of frames for each specified section
celebFrame = LabelFrame(root, bd=10, bg='turquoise')
celebFrame.grid(row=3, column=1, padx=5, pady=20)
 
webFrame = LabelFrame(root, bd=10, bg='turquoise')
webFrame.grid(row=3, column=3, padx=5, pady=20)

genFrame = LabelFrame(root, bd=10, bg='turquoise')
genFrame.grid(row=3, column=5, padx=5, pady=20)

# Design for GUI
myTitleFont = font.Font(family='Helvetica', size=30, weight='bold')
mySubTitleFont = font.Font(family='Helvetica', size=24)
myDescFont = font.Font(family='Helvetica', size=12)
myBtnFont = font.Font(family='Helvetica', weight='bold')

# Creation of Titles and Example Images
lblTitle = Label(root, text="What would your face look like\ncombined with a Celebrity's face?", font=myTitleFont, bg='light blue', borderwidth=5, relief="ridge").grid(row=0, column=3, pady=20)
celeb_title = Label(root, text="Celebrity", font=mySubTitleFont, bg='light blue', borderwidth=5, relief="ridge").grid(row=1, column=1, pady=5)
user_title = Label(root, text="User", font=mySubTitleFont, bg='light blue', borderwidth=5, relief="ridge").grid(row=1, column=3, pady=5)
generated_title = Label(root, text="Generator", font=mySubTitleFont, bg='light blue', borderwidth=5, relief="ridge").grid(row=1, column=5, pady=5)

# GUI Description
celebDesc = Label(root, text="STEP 1: Please select the celebrities from\nthe grid below that you would like\nto merge your face with.", font=myDescFont, bg='turquoise', borderwidth=2, relief="solid").grid(row=2, column=1, pady=10)
webDesc = Label(root, text="STEP 2: Now please click the 'Snapshot' Button, and proceed to take\na snapshot of your face. Please ensure your head is \nfully surrounded by the Orange Box. ", font=myDescFont, bg='turquoise', borderwidth=2, relief="solid").grid(row=2, column=3, pady=10)
genDesc = Label(root, text="STEP 3: Finally, Please press the 'Run StarGAN Model' to generate\nyour images, but make sure you have selected your\nchosen celebrities and taken a Snapshot. Enjoy!", font=myDescFont, bg='turquoise', borderwidth=2, relief="solid").grid(row=2, column=5, pady=10)

# Webcam View

# Creation of Webcam Example images
webExImg = Image.open('exampleImages/WebcamExample.png')
resizedWebEx = webExImg.resize((375, 400), Image.ANTIALIAS)
photoWebEx = ImageTk.PhotoImage(resizedWebEx)

global generated_WebImg
generated_ExampleWebImg = Label(webFrame, image=photoWebEx, text="Example Webcam Snapshot:")
generated_ExampleWebImg.grid(row=0, column=1)

# When the Take Snapshot button is pressed the following function will execute.
def webcam():
    # Enables the image created to be exported to the GUI
    global photoWeb
    # Initialises the Webcam to be used to show it's view.
    cam = cv2.VideoCapture(0)
    # Naming the Webcam Window
    cv2.namedWindow("Webcam Snapshot")
    
    while True:
        # Reading the webcam window
        ret, frame = cam.read()
        image = frame.copy()

        # Error Capture 
        if not ret:
            print("failed to grab frame")
            break
        
        # Converting the frame to Greyscale which is easier for the faces to be detected.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detecting the faces using the Frontal Face Haarcascade
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        
        # For each face detected:
        for (x, y, w, h) in faces:

            # Converts images back to colour and crops the image to the desired size and where face is centered.
            roi_colour = image[y-65:y + h+40, x-40:x + w+45]

            # Displays Rectangle surrounding detected faces on the webcam window
            cv2.rectangle(image, (x-42, y-75), (x + w+47, y + h+47), (0,165,255), 2)

        # Showing what the webcam sees to the user
        cv2.imshow("Webcam Snapshot", image)

        k = cv2.waitKey(10)
        if k%256 == 27:
            # IF ESC pressed Then exit window
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            # Save Source Image to desired directory
            img_name = "assets/representative/custom/src/male/source_frame.png"
            cv2.imwrite(img_name, roi_colour)
            print("Webcam Snapshot written!")
            
            # Delete Example webcam image and replace it with the recently taken snapshot.
            generated_ExampleWebImg.destroy()
            exmpImg = Image.open('assets/representative/custom/src/male/source_frame.png')
            resizedWeb = exmpImg.resize((375, 400), Image.ANTIALIAS)
            photoWeb = ImageTk.PhotoImage(resizedWeb)
            generated_WebImg = Label(webFrame, image=photoWeb)
            generated_WebImg.grid(row=2, column=1, pady=20)
            
    # End capture from the Webcam and close windows        
    cam.release()
    cv2.destroyAllWindows()
            

# Creation of Snapshot button which is responsible for running Webcam() function
btn_snapshot = Button(webFrame, text="Take a Snapshot!", font=myBtnFont, command=webcam, fg="white", bg="grey")
btn_snapshot.grid(row=1, column=1, pady=20)

# Celebrity Image List / Image Viewer

# Opening images from destination to allow for resizing
celebimg1 = Image.open('GUI/celebs/img1.jpg')
celebimg2 = Image.open('GUI/celebs/img2.jpg')
celebimg3 = Image.open('GUI/celebs/img3.jpg')
celebimg4 = Image.open('GUI/celebs/img4.jpg')
celebimg5 = Image.open('GUI/celebs/img5.jpg')
celebimg6 = Image.open('GUI/celebs/img6.jpg')
celebimg7 = Image.open('GUI/celebs/img7.jpg')
celebimg8 = Image.open('GUI/celebs/img8.jpg')
celebimg9 = Image.open('GUI/celebs/img9.jpg')
celebimg10 = Image.open('GUI/celebs/img10.jpg')
celebimg11 = Image.open('GUI/celebs/img11.jpg')
celebimg12 = Image.open('GUI/celebs/img12.jpg')
celebimg13 = Image.open('GUI/celebs/img13.jpg')
celebimg14 = Image.open('GUI/celebs/img14.jpg')
celebimg15 = Image.open('GUI/celebs/img15.jpg')
celebimg16 = Image.open('GUI/celebs/img16.jpg')
celebimg17 = Image.open('GUI/celebs/img17.jpg')
celebimg18 = Image.open('GUI/celebs/img18.jpg')
celebimg19 = Image.open('GUI/celebs/img19.jpg')
celebimg20 = Image.open('GUI/celebs/img20.jpg')
celebimg21 = Image.open('GUI/celebs/img21.jpg')
celebimg22 = Image.open('GUI/celebs/img22.jpg')
celebimg23 = Image.open('GUI/celebs/img23.jpg')
celebimg24 = Image.open('GUI/celebs/img24.jpg')
celebimg25 = Image.open('GUI/celebs/img25.jpg')
celebimg26 = Image.open('GUI/celebs/img26.jpg')
celebimg27 = Image.open('GUI/celebs/img27.jpg')
celebimg28 = Image.open('GUI/celebs/img28.jpg')
celebimg29 = Image.open('GUI/celebs/img29.jpg')
celebimg30 = Image.open('GUI/celebs/img30.jpg')
celebimg31 = Image.open('GUI/celebs/img31.jpg')
celebimg32 = Image.open('GUI/celebs/img32.jpg')
celebimg33 = Image.open('GUI/celebs/img33.jpg')
celebimg34 = Image.open('GUI/celebs/img34.jpg')
celebimg35 = Image.open('GUI/celebs/img35.jpg')
celebimg36 = Image.open('GUI/celebs/img36.jpg')

# Resizing all celebrity images to (width = 100, height = 100)
resizeW = 100
resizeH = 100
resized1 = celebimg1.resize((resizeW, resizeH), Image.ANTIALIAS)
resized2 = celebimg2.resize((resizeW, resizeH), Image.ANTIALIAS)
resized3 = celebimg3.resize((resizeW, resizeH), Image.ANTIALIAS)
resized4 = celebimg4.resize((resizeW, resizeH), Image.ANTIALIAS)
resized5 = celebimg5.resize((resizeW, resizeH), Image.ANTIALIAS)
resized6 = celebimg6.resize((resizeW, resizeH), Image.ANTIALIAS)
resized7 = celebimg7.resize((resizeW, resizeH), Image.ANTIALIAS)
resized8 = celebimg8.resize((resizeW, resizeH), Image.ANTIALIAS)
resized9 = celebimg9.resize((resizeW, resizeH), Image.ANTIALIAS)
resized10 = celebimg10.resize((resizeW, resizeH), Image.ANTIALIAS)
resized11 = celebimg11.resize((resizeW, resizeH), Image.ANTIALIAS)
resized12 = celebimg12.resize((resizeW, resizeH), Image.ANTIALIAS)
resized13 = celebimg13.resize((resizeW, resizeH), Image.ANTIALIAS)
resized14 = celebimg14.resize((resizeW, resizeH), Image.ANTIALIAS)
resized15 = celebimg15.resize((resizeW, resizeH), Image.ANTIALIAS)
resized16 = celebimg16.resize((resizeW, resizeH), Image.ANTIALIAS)
resized17 = celebimg17.resize((resizeW, resizeH), Image.ANTIALIAS)
resized18 = celebimg18.resize((resizeW, resizeH), Image.ANTIALIAS)
resized19 = celebimg19.resize((resizeW, resizeH), Image.ANTIALIAS)
resized20 = celebimg20.resize((resizeW, resizeH), Image.ANTIALIAS)
resized21 = celebimg21.resize((resizeW, resizeH), Image.ANTIALIAS)
resized22 = celebimg22.resize((resizeW, resizeH), Image.ANTIALIAS)
resized23 = celebimg23.resize((resizeW, resizeH), Image.ANTIALIAS)
resized24 = celebimg24.resize((resizeW, resizeH), Image.ANTIALIAS)
resized25 = celebimg25.resize((resizeW, resizeH), Image.ANTIALIAS)
resized26 = celebimg26.resize((resizeW, resizeH), Image.ANTIALIAS)
resized27 = celebimg27.resize((resizeW, resizeH), Image.ANTIALIAS)
resized28 = celebimg28.resize((resizeW, resizeH), Image.ANTIALIAS)
resized29 = celebimg29.resize((resizeW, resizeH), Image.ANTIALIAS)
resized30 = celebimg30.resize((resizeW, resizeH), Image.ANTIALIAS)
resized31 = celebimg31.resize((resizeW, resizeH), Image.ANTIALIAS)
resized32 = celebimg32.resize((resizeW, resizeH), Image.ANTIALIAS)
resized33 = celebimg33.resize((resizeW, resizeH), Image.ANTIALIAS)
resized34 = celebimg34.resize((resizeW, resizeH), Image.ANTIALIAS)
resized35 = celebimg35.resize((resizeW, resizeH), Image.ANTIALIAS)
resized36 = celebimg36.resize((resizeW, resizeH), Image.ANTIALIAS)

# Turning resized image into Photo Images
photo1 = ImageTk.PhotoImage(resized1)
photo2 = ImageTk.PhotoImage(resized2)
photo3 = ImageTk.PhotoImage(resized3)
photo4 = ImageTk.PhotoImage(resized4)
photo5 = ImageTk.PhotoImage(resized5)
photo6 = ImageTk.PhotoImage(resized6)
photo7 = ImageTk.PhotoImage(resized7)
photo8 = ImageTk.PhotoImage(resized8)
photo9 = ImageTk.PhotoImage(resized9)
photo10 = ImageTk.PhotoImage(resized10)
photo11 = ImageTk.PhotoImage(resized11)
photo12 = ImageTk.PhotoImage(resized12)
photo13 = ImageTk.PhotoImage(resized13)
photo14 = ImageTk.PhotoImage(resized14)
photo15 = ImageTk.PhotoImage(resized15)
photo16 = ImageTk.PhotoImage(resized16)
photo17 = ImageTk.PhotoImage(resized17)
photo18 = ImageTk.PhotoImage(resized18)
photo19 = ImageTk.PhotoImage(resized19)
photo20 = ImageTk.PhotoImage(resized20)
photo21 = ImageTk.PhotoImage(resized21)
photo22 = ImageTk.PhotoImage(resized22)
photo23 = ImageTk.PhotoImage(resized23)
photo24 = ImageTk.PhotoImage(resized24)
photo25 = ImageTk.PhotoImage(resized25)
photo26 = ImageTk.PhotoImage(resized26)
photo27 = ImageTk.PhotoImage(resized27)
photo28 = ImageTk.PhotoImage(resized28)
photo29 = ImageTk.PhotoImage(resized29)
photo30 = ImageTk.PhotoImage(resized30)
photo31 = ImageTk.PhotoImage(resized31)
photo32 = ImageTk.PhotoImage(resized32)
photo33 = ImageTk.PhotoImage(resized33)
photo34 = ImageTk.PhotoImage(resized34)
photo35 = ImageTk.PhotoImage(resized35)
photo36 = ImageTk.PhotoImage(resized36)

# Copying Celebrity images from one directory to another
def save_img(img_num):
    if img_num == 1:
        copyfile(('GUI/celebs/img1.jpg'), ('assets/representative/custom/ref/male/img1.jpg'))
    elif img_num == 2:
        copyfile(('GUI/celebs/img2.jpg'), ('assets/representative/custom/ref/female/img2.jpg'))
    elif img_num == 3:
        copyfile(('GUI/celebs/img3.jpg'), ('assets/representative/custom/ref/male/img3.jpg'))
    elif img_num == 4:
        copyfile(('GUI/celebs/img4.jpg'), ('assets/representative/custom/ref/male/img4.jpg'))
    elif img_num == 5:
        copyfile(('GUI/celebs/img5.jpg'), ('assets/representative/custom/ref/female/img5.jpg'))
    elif img_num == 6:
        copyfile(('GUI/celebs/img6.jpg'), ('assets/representative/custom/ref/female/img6.jpg'))
    elif img_num == 7:
        copyfile(('GUI/celebs/img7.jpg'), ('assets/representative/custom/ref/male/img7.jpg'))
    elif img_num == 8:
        copyfile(('GUI/celebs/img8.jpg'), ('assets/representative/custom/ref/female/img8.jpg'))
    elif img_num == 9:
        copyfile(('GUI/celebs/img9.jpg'), ('assets/representative/custom/ref/female/img9.jpg'))
    elif img_num == 10:
        copyfile(('GUI/celebs/img10.jpg'), ('assets/representative/custom/ref/male/img10.jpg'))
    elif img_num == 11:
        copyfile(('GUI/celebs/img11.jpg'), ('assets/representative/custom/ref/male/img11.jpg'))
    elif img_num == 12:
        copyfile(('GUI/celebs/img12.jpg'), ('assets/representative/custom/ref/female/img12.jpg'))
    elif img_num == 13:
        copyfile(('GUI/celebs/img13.jpg'), ('assets/representative/custom/ref/male/img13.jpg'))
    elif img_num == 14:
        copyfile(('GUI/celebs/img14.jpg'), ('assets/representative/custom/ref/female/img14.jpg'))
    elif img_num == 15:
        copyfile(('GUI/celebs/img15.jpg'), ('assets/representative/custom/ref/female/img15.jpg'))
    elif img_num == 16:
        copyfile(('GUI/celebs/img16.jpg'), ('assets/representative/custom/ref/female/img16.jpg'))
    elif img_num == 17:
        copyfile(('GUI/celebs/img17.jpg'), ('assets/representative/custom/ref/female/img17.jpg'))
    elif img_num == 18:
        copyfile(('GUI/celebs/img18.jpg'), ('assets/representative/custom/ref/male/img18.jpg'))
    elif img_num == 19:
        copyfile(('GUI/celebs/img19.jpg'), ('assets/representative/custom/ref/female/img19.jpg'))
    elif img_num == 20:
        copyfile(('GUI/celebs/img20.jpg'), ('assets/representative/custom/ref/female/img20.jpg'))
    elif img_num == 21:
        copyfile(('GUI/celebs/img21.jpg'), ('assets/representative/custom/ref/male/img21.jpg'))
    elif img_num == 22:
        copyfile(('GUI/celebs/img22.jpg'), ('assets/representative/custom/ref/female/img22.jpg'))
    elif img_num == 23:
        copyfile(('GUI/celebs/img23.jpg'), ('assets/representative/custom/ref/female/img23.jpg'))
    elif img_num == 24:
        copyfile(('GUI/celebs/img24.jpg'), ('assets/representative/custom/ref/male/img24.jpg'))
    elif img_num == 25:
        copyfile(('GUI/celebs/img25.jpg'), ('assets/representative/custom/ref/female/img25.jpg'))
    elif img_num == 26:
        copyfile(('GUI/celebs/img26.jpg'), ('assets/representative/custom/ref/male/img26.jpg'))
    elif img_num == 27:
        copyfile(('GUI/celebs/img27.jpg'), ('assets/representative/custom/ref/male/img27.jpg'))
    elif img_num == 28:
        copyfile(('GUI/celebs/img28.jpg'), ('assets/representative/Celebrity/male/img28.jpg'))
    elif img_num == 29:
        copyfile(('GUI/celebs/img29.jpg'), ('assets/representative/custom/ref/male/img29.jpg'))
    elif img_num == 30:
        copyfile(('GUI/celebs/img30.jpg'), ('assets/representative/custom/ref/female/img30.jpg'))
    elif img_num == 31:
        copyfile(('GUI/celebs/img31.jpg'), ('assets/representative/custom/ref/male/img31.jpg'))
    elif img_num == 32:
        copyfile(('GUI/celebs/img32.jpg'), ('assets/representative/custom/ref/male/img32.jpg'))
    elif img_num == 33:
        copyfile(('GUI/celebs/img33.jpg'), ('assets/representative/custom/ref/male/img33.jpg'))
    elif img_num == 34:
        copyfile(('GUI/celebs/img34.jpg'), ('assets/representative/custom/ref/male/img34.jpg'))
    elif img_num == 35:
        copyfile(('GUI/celebs/img35.jpg'), ('assets/representative/custom/ref/male/img35.jpg'))
    elif img_num == 36:
        copyfile(('GUI/celebs/img36.jpg'), ('assets/representative/custom/ref/female/img36.jpg'))
    

# Celebrity Selection Buttons
cBtn1 = Button(celebFrame, image=photo1, height=resizeH, width=resizeW, command=lambda: save_img(1)).grid(row=1, column=1)
cBtn2 = Button(celebFrame, image=photo2, height=resizeH, width=resizeW, command=lambda: save_img(2)).grid(row=1, column=2)
cBtn3 = Button(celebFrame, image=photo3, height=resizeH, width=resizeW, command=lambda: save_img(3)).grid(row=1, column=3)
cBtn4 = Button(celebFrame, image=photo4, height=resizeH, width=resizeW, command=lambda: save_img(4)).grid(row=1, column=4)
cBtn5 = Button(celebFrame, image=photo5, height=resizeH, width=resizeW, command=lambda: save_img(5)).grid(row=1, column=5)
cBtn6 = Button(celebFrame, image=photo6, height=resizeH, width=resizeW, command=lambda: save_img(6)).grid(row=1, column=6)
cBtn7 = Button(celebFrame, image=photo7, height=resizeH, width=resizeW, command=lambda: save_img(7)).grid(row=2, column=1)
cBtn8 = Button(celebFrame, image=photo8, height=resizeH, width=resizeW, command=lambda: save_img(8)).grid(row=2, column=2)
cBtn9 = Button(celebFrame, image=photo9, height=resizeH, width=resizeW, command=lambda: save_img(9)).grid(row=2, column=3)
cBtn10 = Button(celebFrame, image=photo10, height=resizeH, width=resizeW, command=lambda: save_img(10)).grid(row=2, column=4)
cBtn11 = Button(celebFrame, image=photo11, height=resizeH, width=resizeW, command=lambda: save_img(11)).grid(row=2, column=5)
cBtn12 = Button(celebFrame, image=photo12, height=resizeH, width=resizeW, command=lambda: save_img(12)).grid(row=2, column=6)
cBtn13 = Button(celebFrame, image=photo13, height=resizeH, width=resizeW, command=lambda: save_img(13)).grid(row=3, column=1)
cBtn14 = Button(celebFrame, image=photo14, height=resizeH, width=resizeW, command=lambda: save_img(14)).grid(row=3, column=2)
cBtn15 = Button(celebFrame, image=photo15, height=resizeH, width=resizeW, command=lambda: save_img(15)).grid(row=3, column=3)
cBtn16 = Button(celebFrame, image=photo16, height=resizeH, width=resizeW, command=lambda: save_img(16)).grid(row=3, column=4)
cBtn17 = Button(celebFrame, image=photo17, height=resizeH, width=resizeW, command=lambda: save_img(17)).grid(row=3, column=5)
cBtn18 = Button(celebFrame, image=photo18, height=resizeH, width=resizeW, command=lambda: save_img(18)).grid(row=3, column=6)
cBtn19 = Button(celebFrame, image=photo19, height=resizeH, width=resizeW, command=lambda: save_img(19)).grid(row=4, column=1)
cBtn20 = Button(celebFrame, image=photo20, height=resizeH, width=resizeW, command=lambda: save_img(20)).grid(row=4, column=2)
cBtn21 = Button(celebFrame, image=photo21, height=resizeH, width=resizeW, command=lambda: save_img(21)).grid(row=4, column=3)
cBtn22 = Button(celebFrame, image=photo22, height=resizeH, width=resizeW, command=lambda: save_img(22)).grid(row=4, column=4)
cBtn23 = Button(celebFrame, image=photo23, height=resizeH, width=resizeW, command=lambda: save_img(23)).grid(row=4, column=5)
cBtn24 = Button(celebFrame, image=photo24, height=resizeH, width=resizeW, command=lambda: save_img(24)).grid(row=4, column=6)
cBtn25 = Button(celebFrame, image=photo25, height=resizeH, width=resizeW, command=lambda: save_img(25)).grid(row=5, column=1)
cBtn26 = Button(celebFrame, image=photo26, height=resizeH, width=resizeW, command=lambda: save_img(26)).grid(row=5, column=2)
cBtn27 = Button(celebFrame, image=photo27, height=resizeH, width=resizeW, command=lambda: save_img(27)).grid(row=5, column=3)
cBtn28 = Button(celebFrame, image=photo28, height=resizeH, width=resizeW, command=lambda: save_img(28)).grid(row=5, column=4)
cBtn29 = Button(celebFrame, image=photo29, height=resizeH, width=resizeW, command=lambda: save_img(29)).grid(row=5, column=5)
cBtn30 = Button(celebFrame, image=photo30, height=resizeH, width=resizeW, command=lambda: save_img(30)).grid(row=5, column=6)
cBtn31 = Button(celebFrame, image=photo31, height=resizeH, width=resizeW, command=lambda: save_img(31)).grid(row=6, column=1)
cBtn32 = Button(celebFrame, image=photo32, height=resizeH, width=resizeW, command=lambda: save_img(32)).grid(row=6, column=2)
cBtn33 = Button(celebFrame, image=photo33, height=resizeH, width=resizeW, command=lambda: save_img(33)).grid(row=6, column=3)
cBtn34 = Button(celebFrame, image=photo34, height=resizeH, width=resizeW, command=lambda: save_img(34)).grid(row=6, column=4)
cBtn35 = Button(celebFrame, image=photo35, height=resizeH, width=resizeW, command=lambda: save_img(35)).grid(row=6, column=5)
cBtn36 = Button(celebFrame, image=photo36, height=resizeH, width=resizeW, command=lambda: save_img(36)).grid(row=6, column=6)


# Generated Image View / Export
def runStar():
    # Try run the model if it doesnt work create error message
    try:
        # Creating variable which stores the command to be sent to the CMD
        cmd = 'python main.py --mode sample --num_domains 2 --resume_iter 100000 --w_hpf 1 --checkpoint_dir expr/checkpoints/celeba_hq --result_dir expr/results/custom --src_dir assets/representative/custom/src --ref_dir assets/representative/custom/ref'
        os.system(cmd)
        # Once the model has ran show the generated image to the user
        image=Image.open('expr/results/custom/reference.jpg').show()
    except:
        # Show error message if any errors within model
        messagebox.showerror("Error Message", "Please make sure you have selected at least one Celebrity,\nand also ensure you have taken a Snapshot of your face. Thankyou")


# Example Generated Image
exmpImg = Image.open('exampleImages/referenceExample.jpg')
resizedExp = exmpImg.resize((300, 450), Image.ANTIALIAS)
photoExmp = ImageTk.PhotoImage(resizedExp)
 
# Creation of label displayed under button detailing how long it takes to generate
runLbl = Label(genFrame, text="After you have pressed 'Run StarGAN'\nThe image should take around 30 Seconds to generate\nand it will then automatically be displayed for you to see.\n Thankyou :)", font=myDescFont, bg="turquoise")
runLbl.grid(row=5, column=1)

# Shwoing example generated image to give user an idea of what is to come
global generated_img
generated_img = Label(genFrame, image=photoExmp)
generated_img.grid(row=1, column=1)

exampleLbl = Label(genFrame, text="Example of Generated Image:", bg="turquoise", font=myBtnFont)
exampleLbl.grid(row=0, column=1)
# Creation of "Run StarGAN" button containg StarGAN initiation function
btn_run = Button(genFrame, text="Run StarGAN Model", font=myBtnFont, command=runStar, fg="white", bg="grey")
btn_run.grid(row=3, column=1, pady=20)


# Run Main Loop
emptyFolders()
root.mainloop()
