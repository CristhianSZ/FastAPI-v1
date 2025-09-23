import jwt

def createToken(data: dict):
    token : str = jwt.encode(payload=data, key="secret", algorithm="HS256")
    return token

