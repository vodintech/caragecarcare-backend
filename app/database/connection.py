from pymongo import MongoClient
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🔄 Connecting to MongoDB...")
logger.info(f"🔄 Database: {settings.DB_NAME}")

client = MongoClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

# Test connection
try:
    db.command("ping")
    logger.info("✅ MongoDB connection successful!")
except Exception as e:
    logger.error(f"❌ Connection failed: {e}")
    raise