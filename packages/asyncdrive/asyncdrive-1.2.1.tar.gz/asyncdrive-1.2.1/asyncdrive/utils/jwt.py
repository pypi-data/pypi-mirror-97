import base64
import datetime
import io
import json

from OpenSSL import crypto

"""
    Basic implementation of JSON Web Token (JWT)
    as described in Google's documentation (see link below)

    https://developers.google.com/identity/protocols/oauth2/service-account#httprest

    You should not need to call this function directly,
    if you are doing so, you are doing something wrong.
"""

def create_jwt(cred_path, scopes=['https://www.googleapis.com/auth/drive'], sub=None):
    with io.open(cred_path, 'r') as file:
        credentials = json.load(file)

    iat = int(datetime.datetime.now().timestamp())
    header = {"typ": "JWT", "alg": "RS256", "kid": credentials["private_key_id"]}
    claim = {
        "iss": credentials["client_email"],
        "kid": credentials["client_email"],
        "scope": ','.join(scopes),
        "aud": "https://oauth2.googleapis.com/token",
        "exp": iat + 3600,
        "iat": iat
    }
    if sub:
        claim['sub'] = sub

    encoded_header = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    encoded_claim = base64.urlsafe_b64encode(json.dumps(claim, separators=(',', ':')).encode("utf-8"))
    segments = [encoded_header, encoded_claim]

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, credentials["private_key"])
    signing_input = b'.'.join(segments)

    sign = base64.urlsafe_b64encode(crypto.sign(pkey, signing_input, "sha256"))

    segments.append(sign)
    jwt = b'.'.join(segments).decode("utf-8")

    return jwt
