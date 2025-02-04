import base64
import uuid, hmac, hashlib


def generate_transaction_id() -> str:
    return str(uuid.uuid4().hex[:20])

def encode_cips_message(cips_message: str) -> str:
    ...


def encode_esewa_message(message:str, secret)->str:
    hmac_256 = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    digest = hmac_256.digest()
    signature = base64.b64encode(digest).decode("utf-8")
    return signature

def decode_esewa_message(signature, secret)->str:
    ...


def sign_connect_ips_message(cips_message: bytes, certificate_path) -> str:
    with open(certificate_path, "rb") as cert_file:
        cert_data = cert_file.read()

def get_encoded_token_cips(token: str, cert_path) -> str:
    message = token.encode()
    signed_message = sign_connect_ips_message(message, cert_path)
    return signed_message