from werkzeug.security import generate_password_hash, check_password_hash

# convert password to hash value
def encode_password(password):
        hash_password = generate_password_hash(password)
        return hash_password #hash value of password

# Verify if the hash value of password is equal to the input password
def decode_password(hash_password, password):
        check_password = check_password_hash(hash_password, password)
        return check_password #True or False