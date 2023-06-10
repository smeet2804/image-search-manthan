from logging import debug
from re import S
from downloader import Downloader
from scrapper import Scrapper
import os
from flask import Flask, request, jsonify
from PIL import Image
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse,HTMLResponse
import numpy as np
import cv2
from vectorizer_deepface import Vectorizer
import io
from vectorizer_deepface import Vectorizer
import ner
from local_search import Searcher
 


app = FastAPI()
@app.post("/image/search")
async def search_api(file: UploadFile = File(...)):
    dir_name = "temp"
    if not os.path.isdir("Downloads/"+dir_name):
        os.mkdir("Downloads/"+dir_name)

    if len(os.listdir("Downloads/"+dir_name)) != 0:
        for f in os.listdir("Downloads/"+dir_name):
            os.remove(os.path.join("Downloads/"+dir_name, f))

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png","jfif")
    if not extension:
        return "Image must be of proper format!"

    vec = Vectorizer()
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    image.save("query_data/test.jpg") 
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    query_image = np.array(vec.vectorize_single(opencvImage), dtype = np.float32)
    query_image = query_image.reshape(1, 128)
    downloader = Downloader("query_data/test.jpg")

    

    download_dir = "Downloads/"+dir_name
    link_map = downloader.download(dir_name)
    searcher = Searcher(download_dir)
    searcher.input_query_image(query_image)
    searcher.initialize_data_store()
    ret = searcher.search()
    paths = list(ret.keys())
    outputLinks = []
    for path in paths:
        ret[path].append(link_map[path])
        outputLinks.append(link_map[path])

    print(outputLinks)
    names = ner.get_names(outputLinks) 
    ret["names"] = names
    return ret

if __name__ == "__main__":
    uvicorn.run(app, debug=True)

