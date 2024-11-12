from flask import Flask, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()
user = os.getenv("USER")
pw=os.getenv("PASS")

app = Flask(__name__)
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
async def home():
    try:
        document = {
            "embeddings": "Post Title 1",
            "id": "Body of post."
        }

        result = collection.insert_one(document)

        print(result.acknowledged)

        #a = database.collection.find( {"embeddings": "Post Title 1"} )

        #client.close()
        a = database.collection.find({})
        results = collection.find_one({ "embeddings": "Post Title 1" })
        l=[]
        # for i in a:
        #     print(i, flush=True)
        #     l.append(i)
        for i in results:
            l.append(i)
        return results["id"]

    except Exception as e:
        print(e)
        return 'Hello, World!'


#function to upload images and id's to mongodb server
@app.route('/upload', methods=["POST"])
def upload():
    #grab emnbeddings and id from request.body TODO
    id=0
    embeddings=0
    count = collection.count_documents({ "id": id })
    if count==0:
        print(count)
        document = {
            "embeddings": embeddings,
            "id": id
        }
        return 200
    else:
        return 409
    
#TODO
@app.route('/check_id', methods=["GET"])
def checkID():
    #gonna have to implement OPENCV/Facialrecognition libraries to check this
    results = collection.find_one({ "embeddings": "Post Title 1" })
    if(results):
        return id
    else:
        return 404