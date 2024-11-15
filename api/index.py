from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import os
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import face_recognition


load_dotenv()
user = os.getenv("USER")
pw=os.getenv("PASS")

app = Flask(__name__)

database=""
collection=""

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

@app.route('/test')
async def test():
    try:
        document = {
            "embeddings": [
-0.12542816, 0.0652061, 0.12394607, 0.02423882, -0.08168113, 0.01228087, -0.01443338, -0.11215433, 0.19984981, -0.07825743, 0.16019039, 0.02497483, -0.1638823, 0.08152732, -0.07165051, 0.04151121, -0.12665054, -0.08681241, -0.02023332, -0.12555268, 0.03211293, 0.03364171, -0.0618048, -0.00107205, -0.20101814, -0.27922413, -0.08259065, -0.10732785, 0.10351838, -0.05197021, -0.02078326, 0.03370402, -0.14583838, 0.02219997, 0.04582398, 0.03431956, 0.02884571, 0.01754401, 0.18889967, -0.00322025, -0.1391664, 0.03618713, 0.0616816, 0.21097834, 0.16537064, 0.13099001, -0.00756426, -0.10378352, 0.09754878, -0.17788398, 0.03757026, 0.13508025, 0.06225245, 0.06666714, 0.0413729, -0.22560169, -0.03160803, -0.02334791, -0.1824531, 0.12866431, 0.06347475, -0.10380627, -0.05282435, 0.00439168, 0.20403142, 0.09930803, -0.1003943, -0.11790477, 0.1848211, -0.24838838, -0.01500291, 0.04746493, -0.06079706, -0.14784619, -0.19681098, 0.0648348, 0.48041481, 0.17566882, -0.15714394, 0.03415987, -0.03032983, -0.04741704, 0.09904169, 0.09931719, -0.13309522, -0.01780549, 0.00637066, 0.03630227, 0.23629537, 0.07084066, -0.01243448, 0.18567468, -0.01211701, 0.0697848, -0.01082286, 0.01339467, -0.12580273, -0.02445328, -0.06693625, -0.0406842, 0.03563322, -0.01847049, 0.09503315, 0.15868054, -0.22116125, 0.18701367, -0.0545835, -0.06322001, 0.00734232, 0.08494901, -0.06663164, 0.01104206, 0.18594857, -0.2523855, 0.22635087, 0.15666212, 0.04192548, 0.14160854, 0.03779654, 0.04590216, 0.05449094, 0.05995531, -0.14256194, -0.08043612, -0.01090786, -0.17400707, 0.09284517, 0.01759548],
            "id": 1234567,
            "name": "test"
        }

        result = collection.insert_one(document)

        # print(result.acknowledged)

        # #a = database.collection.find( {"embeddings": "Post Title 1"} )

        # #client.close()
        # a = database.collection.find({})
        # results = collection.find_one({ "embeddings": "Post Title 1" })
        # l=[]
        # # for i in a:
        # #     print(i, flush=True)
        # #     l.append(i)
        # for i in results:
        #     l.append(i)
        return str(result.acknowledged)

    except Exception as e:
        print(e)
        return 'Hello, World!'


#function to upload images and id's to mongodb server
@app.route('/upload', methods=["POST"])
def upload():
    #grab emnbeddings and id from request.body TODO
    id=0
    embeddings=0
    name="John"
    #embeddings will be a list containing all embeddings for a face/id
    count = collection.count_documents({ "id": id })
    if count==0:
        print(count)
        document = {
            "embeddings": embeddings,
            "id": id,
            "name":name
        }
        return 200
    else:
        return 409
    
@app.route('/get_faces', methods=["GET"])
def getFaces():
    res = collection.find({})
    return_obj = []
    for a in res:
        return_obj.append(json_util.dumps(a))
    print(return_obj)
    return return_obj
    
@app.route('/check_id', methods=["POST"])
def checkID():
    #gonna have to implement OPENCV/Facialrecognition libraries to check this
    data = request.get_json()
    print(data, flush=True)
    #return 200
    results = collection.find_one({ "embedding": data.embeddings })
    if(results):
        return {
            "id":results["id"],
            "name":results["name"]
            }, 200
    else:
        return 404