import os
import sys
import base64
import json
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# بروتوكول الحماية النووية (Nuclear Security Protocol) - النسخة المصححة
def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def load_secure_data(file_path):
    if not os.path.exists(file_path):
        return None
    
    try:
        keys = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    keys[k.strip()] = v.strip()
        
        required = ['BOT_KEY_1', 'BOT_KEY_2', 'BOT_KEY_3', 'REAL_BOT_TOKEN', 'REAL_ADMIN_IDS', 'CORE_HASH']
        if all(k in keys for k in required):
            # التحقق من بصمة الملف المشفر
            current_hash = calculate_file_hash('encrypted_core.dat')
            if not current_hash or current_hash.lower() != keys['CORE_HASH'].lower():
                print(f"🚨 تنبيه أمني: تم اكتشاف تلاعب! (البصمة الحالية: {current_hash})")
                sys.exit(1)
                
            os.environ["REAL_BOT_TOKEN"] = keys['REAL_BOT_TOKEN']
            os.environ["REAL_ADMIN_IDS"] = keys['REAL_ADMIN_IDS']
            
            # تدمير ملف البيانات فوراً
            try:
                os.remove(file_path)
                print("✅ تم التحقق من سلامة النظام وتدمير ملف المفاتيح.")
            except:
                pass
            return keys['BOT_KEY_1'], keys['BOT_KEY_2'], keys['BOT_KEY_3']
    except Exception as e:
        print(f"❌ فشل بروتوكول الأمان: {e}")
    return None

def run_nuclear_bot():
    key_file = 'env.txt'
    extracted = load_secure_data(key_file)
    
    if not extracted:
        print("❌ خطأ: فشل بدء تشغيل النظام الأمني (تأكد من وجود env.txt ببيانات صحيحة)")
        sys.exit(1)

    key1, key2, key3 = extracted

    try:
        with open('encrypted_core.dat', 'rb') as f:
            encoded_data = f.read()
        
        data = base64.b64decode(encoded_data)

        # فك التشفير الثلاثي
        f3 = Fernet(derive_key(key3, b'salt_3'))
        data = f3.decrypt(data)
        f2 = Fernet(derive_key(key2, b'salt_2'))
        data = f2.decrypt(data)
        f1 = Fernet(derive_key(key1, b'salt_1'))
        decrypted_code = f1.decrypt(data).decode('utf-8')

        # تشغيل الكود في الذاكرة
        exec(decrypted_code, globals())

    except Exception as e:
        print(f"❌ فشل فك التشفير: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_nuclear_bot()
