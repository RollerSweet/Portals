from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from fastapi import APIRouter
from bson.json_util import dumps
import datetime
from fastapi.encoders import jsonable_encoder

vmcreator = APIRouter()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['portals']
collection = db['vm_requests']

@vmcreator.post("/create-vm")
async def create_vm(vm_data: dict):
    print(vm_data)
    vm_data['status'] = 'pending'
    vm_data['creation_date'] = datetime.datetime.now()
    vm_data['last_update_date'] = datetime.datetime.now()
    # Insert the data into the MongoDB collection and get the inserted ID
    result = collection.insert_one(vm_data)
    inserted_id = str(result.inserted_id)
    return {"status": "success", "id": inserted_id}


@vmcreator.get("/get-all")
async def get_all():
    documents = collection.find()
    json_docs = dumps(documents)
    return json_docs