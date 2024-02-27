def decodeToken(token, secret_key):
    import jwt
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.DecodeError as e:
        return e