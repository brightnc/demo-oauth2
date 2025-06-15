import bcrypt
import hashlib

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str,hash_type: str) -> bool:
    password_match = False
    if hash_type == "bcrypt":
            password_match = bcrypt.checkpw(password.encode(), hashed_password.encode())
    else:
            match hash_type:
                case "md5":
                    password_match = hashlib.md5(password.encode()).hexdigest() == hashed_password
                case "sha256":
                    password_match = hashlib.sha256(password.encode()).hexdigest() == hashed_password
                case _:
                    password_match = False
            
    return password_match

