from jwt import encode, decode

def create_token(data : dict):
    Token : str = encode(payload=data,key = "my_secrete_key",algorithm="HS256")
    return Token

def validate_token(token : set) -> dict:
    data : dict = decode(token,key = "my_secrete_key",algorithms = ['HS256'])   
    return data