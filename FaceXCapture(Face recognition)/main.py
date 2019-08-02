import tkinter as tk
#from tkinter import tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
import os
#filename = "1"
class Main(tk.Frame):
    def __init__(self, root):
            super().__init__(root)
            self.init_main()


    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar2 = tk.Frame(bg='#d7d8e0', bd = 2)
        toolbar2.pack(side=tk.TOP, fill=tk.X)
        toolbarmain = tk.Frame(bg='#d7d8e0', bd = 2)
        toolbarmain.pack(side= tk.TOP, fill=tk.X)

        #comments like im doing something but of course , its may can be so cool, in the next time we need to do soemthi
        self.add_img=tk.PhotoImage(file="images.png")
        self.add_img2= tk.PhotoImage(file = "obj.png")
        btn_open_dialog = tk.Button(toolbar, text="Photo face scan", command = self.open_dialog, bg = '#d7d8e0', bd =0,compound = tk.TOP, image = self.add_img)
        btn_open_dialog.pack(side = tk.LEFT)
        btn_open_dialog2 = tk.Button(toolbar2, text="Photo object scan", command=self.open_dialog2, bg='#d7d8e0', bd=0,compound=tk.TOP, image=self.add_img2)
        btn_open_dialog2.pack(side = tk.LEFT)

        self.imgclass = tk.PhotoImage(file = "obj.png")
        ##btn_action = tk.Button(toolbarmain, text = "6a class", command=self.open_action, bg='#d7d8e0', bd=0,compound=tk.TOP, image=self.imgclass)
        #btn_action.pack(side = tk.RIGHT)

        self.imgSomething = tk.PhotoImage(file = "obj.png")
        btn_open_dialog = tk.Button(toolbar, text = "Object video scan")
    def open_action(self):
        print("22")

    def open_dialog(self):

        filename = askopenfilename()
        global photo
        photo = filename
        print(filename)
        if ".jpg" in filename:
            print("OK")
            #os.system("find /home/opencv/PycharmProjects/gui2/bb.jpg")
            os.system("cd && python3 -m venv venv && source venv/bin/activate && cd && cd PycharmProjects/gui2 && python identify_face_image.py --image" + " " + filename + " ")

        else:
            mb.showerror("Input Error", "Image must be .jpg file")
        #os.system('cd && cd PycharmProjects/gui/Videorecog/ && python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle')


    def open_dialog2(self):
        print("234")
        #os.system('cd && cd PycharmProjects/gui/Objectrecog && python deep_learning_object_detection.py --image images/example_06.jpg --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel')

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title('Add')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        self.configure(background='white')

if __name__ == "__main__":
        root = tk.Tk()
        app = Main (root)
        app.pack()
        root.title("FaceXCapture")
        root.configure(background='#d7d8e0')
        root.geometry("650x450+300+200")
        root.resizable(False, False)
        root.mainloop()
        print("JJJ")
        print(photo)