from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["demo"]
calls_collection = db["diallo"]

def update_data(
    agent_name: str,
    patient_name: str,
    agent_phone_number: str,
    analystics: str,
    transcribe: str
):
    
    try:
        result = calls_collection.insert_one(
            {
                "agent_name": agent_name,
                "patient_name": patient_name,
                "agent_phone_number": agent_phone_number,
                "analysis": analystics,
                "transcribe": transcribe,
                "created_at": datetime.now()
            }
        )

        if result:
            return str(result.inserted_id)
        
        return None
        
    except Exception as e:
        print(f"[General Error] {e}")
        return None
    
def get_data_by_id(id: str):
    try:
        doc = calls_collection.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])  # convert ObjectId to string for JSON serialization
        return doc
    except Exception as e:
        print(f"[General Error] {e}")
        return None
    
def get_all_docs():
    try:
        docs_cursor = calls_collection.find(
            {},
            {
                "agent_name": 1,
                "patient_name": 1,
                "agent_phone_number": 1,
                "created_at": 1
            }
        ).sort("created_at", -1)

        docs_list = []
        for doc in docs_cursor:
            docs_list.append({
                "_id": str(doc["_id"]),
                "agent_name": doc.get("agent_name"),
                "patient_name": doc.get("patient_name"),
                "agent_phone_number": doc.get("agent_phone_number"),
                "created_at": doc.get("created_at")
            })

        return docs_list

    except Exception as e:
        print(f"[General Error] {e}")
        return None