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
agents_collection = db["diallo_agent"]

def list_agents():
    try:
        docs_cursor = agents_collection.find({}, {"_id": 0, "name": 1})
        return [doc.get("name", "") for doc in docs_cursor]
    except Exception as e:
        print(f"[General Error] {e}")
        return None
    
def get_or_create_agent(agent_name: str):
    try:
        agent = agents_collection.find_one({"name": agent_name})
        if agent:
            return str(agent["_id"])
        else:
            result = agents_collection.insert_one({
                "name": agent_name,
                "created_at": datetime.now()
            })
            return str(result.inserted_id)
    except Exception as e:
        print(f"[General Error] {e}")
        return None

def update_data(
    agent_name: str,
    agent_id: str,
    bucket: str,
    patient_name: str,
    agent_phone_number: str,
    analystics: str,
    transcribe: str
):
    
    try:
        result = calls_collection.insert_one(
            {
                "agent_id": ObjectId(agent_id),
                "agent_name": agent_name,
                "patient_name": patient_name,
                "bucket": bucket,
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
            doc["_id"] = str(doc["_id"])
            doc["agent_id"] = str(doc["agent_id"])
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
                "created_at": 1,
                "bucket": 1
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