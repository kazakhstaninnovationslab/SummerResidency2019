from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import csv
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from PIL import *
from tkinter import *
import tensorflow as tf
from scipy import misc
import cv2
import numpy as np
import facenet
import detect_face
import os
import time
import pickle
import sys
import time


globalresult = ""


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

        self.imgclass = tk.PhotoImage(file = "obj2.png")
        ##btn_action = tk.Button(toolbarmain, text = "6a class", command=self.open_action, bg='#d7d8e0', bd=0,compound=tk.TOP, image=self.imgclass)
        #btn_action.pack(side = tk.RIGHT)

        self.imgSomething = tk.PhotoImage(file = "obj2.png")
        btn_open_dialog = tk.Button(toolbar, text = "Dataset loading and Model training")
    def open_action(self):
        print("22")

    def open_dialog(self):

        filename = askopenfilename()
        print(filename)
        if ".jpg" in filename:
            print("OK")
            img_path = filename
            modeldir = './model/20170511-185253.pb'
            classifier_filename = './class/classifier.pkl'
            npy = './npy'
            train_img = "./train_img"

            with tf.Graph().as_default():
                gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
                sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
                with sess.as_default():
                    pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)

                    minsize = 20  # minimum size of face
                    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
                    factor = 0.709  # scale factor
                    margin = 44
                    frame_interval = 3
                    batch_size = 1000
                    image_size = 182
                    input_image_size = 160

                    HumanNames = os.listdir(train_img)
                    HumanNames.sort()

                    print('Loading feature extraction model')
                    facenet.load_model(modeldir)

                    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                    embedding_size = embeddings.get_shape()[1]

                    classifier_filename_exp = os.path.expanduser(classifier_filename)
                    with open(classifier_filename_exp, 'rb') as infile:
                        (model, class_names) = pickle.load(infile)

                    #video_capture = cv2.VideoCapture("akshay_mov.mp4")
                    c = 0

                    print('Start Recognition!')
                    prevTime = 0
                    # ret, frame = video_capture.read()
                    frame = cv2.imread(img_path, 0)

                    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # resize frame (optional)

                    curTime = time.time() + 1  # calc fps
                    timeF = frame_interval

                    if (c % timeF == 0):
                        find_results = []

                        if frame.ndim == 2:
                            frame = facenet.to_rgb(frame)
                        frame = frame[:, :, 0:3]
                        bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                        nrof_faces = bounding_boxes.shape[0]
                        print('Face Detected: %d' % nrof_faces)

                        if nrof_faces > 0:
                            det = bounding_boxes[:, 0:4]
                            img_size = np.asarray(frame.shape)[0:2]

                            cropped = []
                            scaled = []
                            scaled_reshape = []
                            bb = np.zeros((nrof_faces, 4), dtype=np.int32)

                            for i in range(nrof_faces):
                                emb_array = np.zeros((1, embedding_size))

                                bb[i][0] = det[i][0]
                                bb[i][1] = det[i][1]
                                bb[i][2] = det[i][2]
                                bb[i][3] = det[i][3]

                                # inner exception
                                if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(
                                        frame):
                                    print('face is too close')
                                    continue

                                cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
                                cropped[i] = facenet.flip(cropped[i], False)
                                scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
                                scaled[i] = cv2.resize(scaled[i], (input_image_size, input_image_size),
                                                       interpolation=cv2.INTER_CUBIC)
                                scaled[i] = facenet.prewhiten(scaled[i])
                                scaled_reshape.append(scaled[i].reshape(-1, input_image_size, input_image_size, 3))
                                feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                                emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                                predictions = model.predict_proba(emb_array)
                                #print(predictions)
                                best_class_indices = np.argmax(predictions, axis=1)
                                #print(best_class_indices)
                                best_class_probabilities = predictions[
                                    np.arange(len(best_class_indices)), best_class_indices]
                                #print(best_class_probabilities)
                                cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0),
                                              2)  # boxing face

                                # plot result idx under box
                                text_x = bb[i][0]
                                text_y = bb[i][3] + 20
                                print('Result Indices: ', best_class_indices[0])
                                print(HumanNames)
                                for H_i in HumanNames:
                                    print(H_i)
                                    if HumanNames[best_class_indices[0]] == H_i:
                                        result_names = HumanNames[best_class_indices[0]]
                                        cv2.putText(frame, result_names, (text_x, text_y),cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=1, lineType=2)
                                        print("RES NAME = " + result_names)

                                        #global result
                                        #globalresult = result
                                        result = result_names
                                        print(type(result.split('_')))
                                        str = result.split('_')
                                        name_str = str[0]
                                        id_str = str[1]
                                        id_int = int(id_str)
                                        print(id_int)
                                        with open(r"schooldata.csv", "a", encoding='utf-8') as file:
                                            a_pen = csv.writer(file)
                                            now = datetime.now()
                                            auth_time = now.strftime("%H:%M")
                                            a_pen.writerow((name_str + "", id_int , auth_time , "True"))
                                            file.close()


                        else:
                            print('Unable to align')
                    cv2.imshow('Image', frame)

                    if cv2.waitKey(1000000) & 0xFF == ord('q'):
                        sys.exit("Thanks")
                        #cv2.destroyAllWindows()

            #os.system("find /home/opencv/PycharmProjects/gui2/bb.jpg")


        else:
            mb.showerror("Input Error", "Image must be .jpg file")
        #os.system('cd && cd PycharmProjects/gui/Videorecog/ && python recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle')


    def open_dialog2(self):

        os.system('python3 -m venv venv && source venv/bin/activate && cd && cd PycharmProjects/gui2/ && python data_preprocess.py && cd PycharmProjects/gui2/python train_model.py')
        mb.showinfo("Success", "Your data imported! ")


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title('Add')
        self.lable(globalresult)
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
        #root.iconbitmap('@/home/opencv/PycharmProjects/gui2/logo(1).xbm')
        #img = PhotoImage(file = '/home/opencv/PycharmProjects/logo.ico')
        #root.tk.call('wm', 'iconphoto' , root._w, tk.PhotoImage(Image.open('./PycharmProjects/logo.ico')))
        #root.iconbitmap("/home/opencv/PycharmProjects/logo.ico")
        root.configure(background='#d7d8e0')
        root.geometry("650x450+300+200")
        root.resizable(False, False)
        root.mainloop()
        #Power BI (Microsoft)
