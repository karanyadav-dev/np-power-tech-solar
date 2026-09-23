"""
NP POWER TECH SOLAR - Frontend Configuration
Reads from environment variables only.
NEVER contains database credentials or backend secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file (dev only)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment."""

    # ---------- App ----------
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8080"))
    APP_TITLE: str = os.getenv("APP_TITLE", "NP POWER TECH SOLAR")

    # ---------- Backend API ----------
    BACKEND_API_BASE_URL: str = os.getenv("BACKEND_API_BASE_URL", "http://localhost:3000")
    BACKEND_API_TIMEOUT: int = int(os.getenv("BACKEND_API_TIMEOUT", "30"))

    # ---------- Public Config (safe to expose) ----------
    PUBLIC_COMPANY_NAME: str = os.getenv("PUBLIC_COMPANY_NAME", "NP POWER TECH SOLAR")
    PUBLIC_COMPANY_PHONE: str = os.getenv("PUBLIC_COMPANY_PHONE", "")
    PUBLIC_COMPANY_EMAIL: str = os.getenv("PUBLIC_COMPANY_EMAIL", "")
    PUBLIC_COMPANY_WHATSAPP: str = os.getenv("PUBLIC_COMPANY_WHATSAPP", "")
    PUBLIC_COMPANY_ADDRESS: str = os.getenv("PUBLIC_COMPANY_ADDRESS", "")

    # ---------- i18n ----------
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES: list = os.getenv("SUPPORTED_LANGUAGES", "en,hi").split(",")

    # ---------- Paths ----------
    BASE_DIR: Path = BASE_DIR
    ASSETS_DIR: Path = BASE_DIR / "assets"
    STATIC_DIR: Path = BASE_DIR / "static"
    I18N_DIR: Path = BASE_DIR / "i18n"

    # ---------- Debug ----------
    IS_DEV: bool = APP_ENV == "development"
    IS_PROD: bool = APP_ENV == "production"


settings = Settings()