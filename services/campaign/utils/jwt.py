import jwt


def decode_jwt(token, secret_key, algorithms=('HS256',)):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms, audience="http://127.0.0.1:8000")
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except Exception as e:
        print(e)
        raise ValueError('Invalid token')

