# ============================================================
# config.py
# Configuration File for Charity Blockchain Platform
# ============================================================

import os

# ── Flask Configuration ───────────────────────────────────────
DEBUG = True
TESTING = False
SECRET_KEY = "charity_blockchain_secret_2024_change_in_production"

# ── Server Configuration ──────────────────────────────────────
HOST = "127.0.0.1"
PORT = 8080

# ── Database Configuration ────────────────────────────────────
DATA_FILE = "data.json"

# ── Blockchain Configuration ──────────────────────────────────
BLOCKCHAIN_DIFFICULTY = 2  # Number of leading zeros in hash
BLOCKCHAIN_TOLERANCE = 0.33  # Byzantine fault tolerance threshold

# ── Authentication Configuration ──────────────────────────────
SESSION_TIMEOUT = 60  # Minutes
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 30  # Minutes
PASSWORD_MIN_LENGTH = 8
PASSWORD_HASH_ITERATIONS = 100000

# ── Logging Configuration ─────────────────────────────────────
LOG_FILE = "charity_blockchain.log"
LOG_LEVEL = "INFO"

# ── Security Configuration ────────────────────────────────────
CORS_ENABLED = False
CSRF_PROTECTION = True
SECURE_COOKIES = False  # Set to True in production with HTTPS

# ── Feature Flags ─────────────────────────────────────────────
ENABLE_REGISTRATION = True
ENABLE_DONATIONS = True
ENABLE_FUND_RELEASE = True
ENABLE_AUDIT_LOG = True
ENABLE_FRAUD_DETECTION = True

# ── Fraud Detection Thresholds ────────────────────────────────
FRAUD_LARGE_DONATION_THRESHOLD = 10000  # USD
FRAUD_DONATION_RATE_LIMIT = 100  # Max donations per donor
FRAUD_SUSPICIOUS_NAME_MIN_LENGTH = 2

# ── Email Configuration (Optional) ────────────────────────────
SMTP_SERVER = ""
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
EMAIL_FROM = "noreply@charityblockchain.org"

# ── Defaults ──────────────────────────────────────────────────
DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEZONE = "UTC"

print("✅ Configuration loaded successfully")
