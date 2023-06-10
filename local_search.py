from datastore import Datastore
from vectorizer_deepface import Vectorizer
from PIL import Image
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import time
# from deepface import DeepFace
import tensorflow as tf

# my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
# tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')





class Searcher:
    def __init__(self, dir_path) -> None:
        self.dir_path = dir_path
        self.query_image = None
        self.vec = Vectorizer()
        self.data_store = Datastore()
        self.found = []
        self.results = []        
        self.query_image_path = None

    def input_query_image(self, img_file):

        # self.query_image = Image.open(query_image_path)
        # opencv_query_Image = cv2.cvtColor(np.array(self.query_image), cv2.COLOR_RGB2BGR)

        # self.query_image = np.array(self.vec.vectorize_single(opencv_query_Image), dtype = np.float32)
        # self.query_image = self.query_image.reshape(1, 128)
        self.query_image = img_file

    def initialize_data_store(self):
        onlyfiles = [f for f in listdir(self.dir_path) if isfile(join(self.dir_path, f))]
        self.found = []
        err_count = 0
        count = 0 
        for val in onlyfiles:
            try :
                image = Image.open(self.dir_path+"/"+val)
    

                opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
                embedding = np.array(self.vec.vectorize_single(opencvImage), dtype=np.float32)
                embedding = embedding.reshape(1, 128)
                self.data_store.add(embedding, count, "")

                self.found.append(self.dir_path+"/"+val)
                count+=1

            except Exception as e:
                print(e)
                err_count+=1
                # print(err_count)
                continue
    
    def search(self):
        ret = dict()
        print(type(self.query_image))
        Distances, Identifiers = self.data_store.search(self.query_image)
        endtime = time.time()
        # print(f"time taken {endtime-starttime}")
        # print(Distances, Identifiers) 
        # print(link_maps)
        
        for val, dis in zip(Identifiers[0], Distances[0]):
            if val != -1:
                self.results.append((self.found[val]))
                print(self.found[val], dis)
                ret[self.found[val]] = [str(dis)]
        
        return ret 
        # for val in self.results:
            # metrics = DeepFace.verify(img1_path=self.query_image_path, img2_path=val)
            # print(metrics)
            

        
if __name__ == "__main__":
    # dir_path = input("\n\nEnter Directory Path ===> ")
    dir_path = "Downloads/mukes"
    searcher = Searcher(dir_path)
    # query_image_path = input("\n\nEnter query iamge path ===> ")
    query_image_path = "test_data/muk.jpg"
    searcher.input_query_image(query_image_path)
    searcher.initialize_data_store()
    searcher.search()

