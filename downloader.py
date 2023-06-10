import time
from bs4 import *
import json
import requests
import os
from scrapper import Scrapper
from PIL import Image
import numpy as np
import cv2
from vectorizer_deepface import Vectorizer

class Downloader:
    def __init__(self, file_path) -> None:
        self.scrapper = Scrapper(file_path)
        self.main_urls = self.scrapper.links_target
        self.img_links = self.scrapper.img_links
        self.link_imagePath_maps = dict()
        self.vec = Vectorizer()

    def download(self, dir_name):
        img_count = 0
        img_link_map = dict()
        for link in self.img_links:
            try:
                print(link)
                if link.split(".")[-1] in ("jpg", "jpeg", "png","jfif"):
                    try:
                        time.sleep(0.1)
                        r = requests.get(link)
                        image_path = os.path.join("Downloads", dir_name, str(img_count)+".jpg") 
                        img_count+=1

                        with open(image_path, "wb") as outFile:
                            outFile.write(r.content)
                            outFile.close()
                        try: 
                            query_image = Image.open(image_path)
                            opencv_query_Image = cv2.cvtColor(np.array(query_image), cv2.COLOR_RGB2BGR)

                            query_image = self.vec.vectorize_single(opencv_query_Image)
                            img_link_map[image_path] = link
                        except Exception as e:
                            print(e)
                            print("Garbage Image")
                            img_link_map.pop(image_path)
                            if os.path.exists(image_path):
                                os.remove(image_path)


                        self.link_imagePath_maps[link] = image_path


                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
                continue
        return img_link_map


if __name__ == "__main__":
    downloader = Downloader()
    dir_name = input("Enter the dir name to store results  ==> ")
    os.mkdir("Downloads/"+dir_name)
    downloader.download(dir_name)
    # print(downloader.imageList)