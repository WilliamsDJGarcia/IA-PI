import cv2
import numpy
import glob
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

def generalFormula():
    Fi = 1
    for i in range(0, len(arrayImg)):      
        Ii = numpy.array(arrayImg[i],dtype=numpy.uint8)
        Fi = alpha*(Fi-1)+((1-alpha)*Ii)
        cv2.imwrite("resultado"+str(i)+".jpg", Fi)

def converVideo():
    for filename in glob.glob('resultado' + '*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter('video.mp4',cv2.VideoWriter_fourcc(*'DIVX'),10, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    cv2.destroyAllWindows()
    out.release()

def select():
    count=0
    path.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4 files",".mp4"),("all files",".*")))
    print (path.filename)
    ls=path.filename
    vidcap = cv2.VideoCapture(ls)
    
    while(vidcap.isOpened()):
        count += 1
        vidcap.set(cv2.CAP_PROP_POS_MSEC,round(count, 2)*1000)
        hasFrames,image = vidcap.read()

        if hasFrames:
            img = cv2.imwrite("Test"+str(count)+".jpg", image) 
            arrayImg.append(image)
        else:
            print(f'YA ACABO')
            vidcap.release()
            cv2.destroyAllWindows()
    generalFormula()
    converVideo()

if __name__ == '__main__':

    arrayImg = []
    img_array = []
    alpha=0.97

    path = Tk()
    path.geometry('200x200')
    path.configure(bg = 'azure')
    path.title('Selección de video')
    ttk.Button(path, text='Seleccionar video', command=select ).pack(side=BOTTOM)
    path.after(3000, lambda: path.destroy()) # Destroy the widget after 30 seconds
    path.mainloop()
