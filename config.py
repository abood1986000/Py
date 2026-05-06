import os

# Bot Configuration
BOT_TOKEN = "8417100081:AAFMjsInjV2anAZmWAoNkKmMA9MVxtpHcjI"
ADMIN_IDS = [7170744706]

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILES_DIR = os.path.join(BASE_DIR, "user_files")

# Limits
FREE_PLAN_LIMITS = {
    "max_files": 5,
    "max_folders": 2,
    "max_file_size": 5 * 1024 * 1024,  # 5MB
}

PRO_PLAN_LIMITS = {
    "max_files": 50,
    "max_folders": 10,
    "max_file_size": 50 * 1024 * 1024,  # 50MB
}
