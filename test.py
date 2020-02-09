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
    path.destroy()

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
    imgAdd()

def imgAdd():
    example = "resultado"+str(len(img_array)-1)+".jpg"
    print(f'VALOR EXAMPLE {example}')
    # Carga de imagen y agregación de evento al mouse
    image = cv2.imread(example)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)

    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("s"):
            image = clone.copy()
            break
    # Se muestra la imagen recortada
    if len(ref_point) == 2:
        crop_img = clone[ref_point[0][1]:ref_point[1]
                        [1], ref_point[0][0]:ref_point[1][0]]
        cv2.imwrite("corte.jpg", crop_img)
        cv2.imshow("crop_img", crop_img)
        cv2.waitKey(0)
        print(f'CROP IMAGE {crop_img}')

def shape_selection(event, x, y, flags, param):
    example = "resultado"+str(len(img_array)-1)+".jpg"
    image = cv2.imread(example)
    # grab references to the global variables
    global ref_point, cropping

    # Seleccion de coordenadas ok
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True
        
    # Seleccion de coordenadas No ok
    elif event == cv2.EVENT_LBUTTONUP:
        # Seleccion x,y
        # Termina corte
        ref_point.append((x, y))
        cropping = False

        # Rectangulo
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

if __name__ == '__main__':

    arrayImg = []
    img_array = []
    alpha=0.97
    ref_point = []
    cropping = False
    example=0
    img=0
    
    path = Tk()
    path.geometry('100x100')
    path.configure(bg = 'azure')
    path.title('Selección de video')
    ttk.Button(path, text='Seleccionar video', command=select ).pack(side=BOTTOM)
    path.mainloop()
