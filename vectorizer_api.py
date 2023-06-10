from re import I
from flask import Flask, request, jsonify
from PIL import Image
from datastore import Datastore
from vectorizer_deepface import Vectorizer
import uvicorn
from fastapi import FastAPI, File, UploadFile, Response
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse,HTMLResponse
import io
import cv2
import numpy as np
import utils
import time

app = FastAPI()

file_name_mappings = utils.get_file_name_mappings()
mappings = utils.get_mappings()

@app.post("/vectorize/image")
async def vectorize_api(identifier: int, file: UploadFile = File(...)):
    ret = {}
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png","jfif")
    if not extension:
        return "Image must be of proper format!"
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    vec = Vectorizer()    
    embeddings = vec.vectorize_single(opencvImage)
    ret["id"] = identifier
    ret["embeddings"] = embeddings
    print(ret)    
    return ret 

@app.post("/vectoriz/search")
async def search_api(file: UploadFile = File(...)):
    ret = {}
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png", "jfif")
    if not extension:
        return "Image must be of proper format"

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    vec = Vectorizer()
    store = Datastore()
    
    emb = np.array(vec.vectorize_single(opencvImage), dtype = np.float32)
    emb = emb.reshape(1, 128)
    starttime = time.time()
    Distances, Identifiers = store.search(emb)
    endtime = time.time()
    print(f"time taken {endtime-starttime}")
    print(Distances, Identifiers) 
    # print(type(Identifiers[0][0]))
    # print(type(Distances[0][0]))
    paths = [file_name_mappings[str(idx)] for idx in Identifiers[0]]


    possible_names = [mappings[str(idx)] for idx in Identifiers[0]]


    ret["ids"] = Identifiers[0].tolist()
    ret["distance"] = Distances[0].tolist()
    ret["results"] = possible_names
    ret["paths"] = paths    

    return ret
    


    

    


if __name__ == "__main__":
    uvicorn.run(app, debug=True)