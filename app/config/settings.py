from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"

if not ENV_PATH.exists():
    raise FileNotFoundError(f"❌ .env not found at: {ENV_PATH}")

load_dotenv(ENV_PATH, override=True)

# Database settings
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://vodintech:ia7m4AaQ8TlMyWid@cluster0.ratvxur.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "carbrands")

# Media settings
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

class Settings:
    MONGODB_URI = MONGODB_URI
    DB_NAME = DB_NAME
    MEDIA_ROOT = MEDIA_ROOT
    MEDIA_URL = MEDIA_URL

settings = Settings()