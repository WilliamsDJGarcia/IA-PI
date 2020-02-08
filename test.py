import cv2
import numpy
import glob
from tkinter import *

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    
    if hasFrames:
        img = cv2.imwrite("Test"+str(count)+".jpg", image) 
        arrayImg.append(image)
        #dataA = np.array(arrayImg[count],dtype=np.uint8)
        #print("Valor del Array:::       ", dataA)
    else:
        print(f'YA ACABO')
        vidcap.release()
        cv2.destroyAllWindows()

def generalFormula():
    Fi = 1
    for i in range(0, len(arrayImg)):      
        Ii = numpy.array(arrayImg[i],dtype=numpy.uint8)
        Fi = alpha*(Fi-1)+((1-alpha)*Ii)
        #print("\nFi:::  ", Ii , "\n")
        cv2.imwrite("resultado"+str(i)+".jpg", Fi)
        # cv2.waitKey(0) 
        # &0;0;0;0;0; 0xff
        pass
    return None

def converVideo():
    for filename in glob.glob('resultado' + '*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter('video.mp4',cv2.VideoWriter_fourcc(*'DIVX'),10, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
        pass
    cv2.destroyAllWindows()
    out.release()
    return None


if __name__ == '__main__':

    vidcap = cv2.VideoCapture('test.mp4')
    arrayImg = []
    img_array = []
    alpha=0.97
    count=0
    success = getFrame(count)

    while(vidcap.isOpened()):
        count += 1
        getFrame(round(count, 2))
    generalFormula()
    converVideo()