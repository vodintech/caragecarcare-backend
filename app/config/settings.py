from dotenv import load_dotenv
from pathlib import Path
import os

# Absolute path to .env (adapt this exact path)
ENV_PATH = Path(r"C:\Users\sitharth\OneDrive\Desktop\caragecarcare-backend\.env")

if not ENV_PATH.exists():
    raise FileNotFoundError(f"❌ .env not found at: {ENV_PATH}")

load_dotenv(ENV_PATH, override=True)

# Debug: Force-check environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

print(f"🔍 .env location: {ENV_PATH}")
print(f"🔍 MONGODB_URI loaded: {'Yes' if MONGODB_URI else 'No'}")

class Settings:
    MONGODB_URI = MONGODB_URI or "mongodb+srv://vodintech:ia7m4AaQ8TlMyWid@cluster0.ratvxur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = DB_NAME or "carbrands"

settings = Settings()