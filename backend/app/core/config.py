import certifi
from pymongo import MongoClient

client = None

def init_db():
    global client
    try:
        uri = "mongodb+srv://raguser:Rag12345%40secure@cluster0.wi6ogu5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
        # Test connection
        client.admin.command("ping")
        print("✅ MongoDB connected successfully")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        client = None

def get_db():
    return client
