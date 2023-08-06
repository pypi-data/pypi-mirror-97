import random
import string
import hashlib
import json

class Validation:
    @staticmethod
    def get_secret(length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    @staticmethod
    def validate_result(result, secret):
        if type(result) != str:
            result = json.dumps(result, indent=4)
        h = hashlib.sha256()
        h.update(result.encode("ascii", 'ignore'))
        h.update(secret.encode("ascii"))
        return h.hexdigest()
    
    @staticmethod
    def validate_result_file(result_path, secret_path, secret):
        if not secret_path.is_file():
            return False
        with open(result_path) as f:
            result = f.read()
        with open(secret_path) as f:
            read_secret = f.read()
            if Validation.validate_result(result, secret) != read_secret:
                return False
        return True

class FailedValidation(Exception):
    pass