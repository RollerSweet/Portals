from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['portals']
collection = db['vm_requests']

# Search for a document by its _id
document_id = ObjectId('644eda2107e2fd11acaf5d68')
query = {'_id': document_id}
result = collection.find_one(query)

# Print the result
print(result)
