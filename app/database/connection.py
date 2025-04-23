from pymongo import MongoClient
from app.config import settings

print("🔄 Connecting to MongoDB...")
print(f"🔄 Database: {settings.DB_NAME}")

client = MongoClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

# Test connection
try:
    db.command("ping")
    print("✅ MongoDB connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    raise