import bcrypt

# hasing the given password
def hashPassword(password):
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd

# checking the given string with hash
def checkPassword(original_pwd,hashed_pwd):
    return bcrypt.checkpw(original_pwd.encode('utf-8'), hashed_pwd)
