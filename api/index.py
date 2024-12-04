from flask import Flask, jsonify, request, Response
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import os
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import face_recognition
import base64
from PIL import Image
import io
import cv2


load_dotenv()
user = os.getenv("USER")
pw=os.getenv("PASS")

app = Flask(__name__)
CORS(
 app,
 resources={
  r"/*": {
   "origins": "*",
   "methods": [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
   ],
   "allow_headers": [
    "Content-Type",
    "Authorization",
    "Access-Control-Allow-Origin"
   ],
  }
 },
)

#https://stackoverflow.com/questions/25186591/having-cv2-imread-reading-images-from-file-objects-or-memory-stream-like-data-h
def np_from_img(file):
     '''converts a buffer from a tar file in np.array'''
     nparr = np.frombuffer(file, np.uint8)
     img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
     return img_np


@app.before_request
def connect_db():
    global collection
    global database
    uri = "mongodb+srv://"+user+":"+pw+"@facial-recognition.snpuh.mongodb.net/?retryWrites=true&w=majority&appName=facial-recognition"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!", flush=True)
    except Exception as e:
        print(e, flush=True)

    database = client.get_database("facial_rec")
    collection = database["faceID"]


@app.route('/')
def home():
    return "hello world!"

#function to upload images and id's to mongodb server
@app.route('/upload', methods=["POST"])
def upload():
    data = request.get_json()
    name=data["name"]
    id=data["id"]
    images=data["images"]
    embeddings=[]
    for i in images:
        image = np_from_img(base64.b64decode(i))
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        x = face_recognition.face_encodings(rgb_img)
        if(len(x)==0):
            return Response(response="not a proper face image!", status=422)
        embeddings.append(x[0].tolist())
        
    print(embeddings)
    print(data["name"], flush=True)

    document = {
        "embeddings": embeddings,
        "id": id,
        "name":name
    }

    result = collection.insert_one(document)
    print(result.acknowledged)

    return Response(response="added to db!", status=200)
    
@app.route('/get_faces', methods=["GET"])
def getFaces():
    res = collection.find({})
    return_obj = []
    for a in res:
        return_obj.append(json_util.dumps(a))
    print(return_obj)
    return return_obj