# jwt/tok.py
import jwt
from password_gen import generate_password as pwd
# print(pwd.__doc__)

secret = pwd(length=14, upper=1, digits=1, special=1, cnt=1)
print(secret)

data = {'payload': secret, 'id': 123456789}
token = jwt.encode(data, secret)
algs = ['HS256', 'HS512']
data_out = jwt.decode(token, secret, algorithms=algs)
print(token)
print()
print(data_out)
