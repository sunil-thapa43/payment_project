import base64
import binascii
import uuid, hmac, hashlib
import requests
from cryptography.hazmat.primitives.serialization import pkcs12

from utils.decorators_ import retry_request


def generate_transaction_id() -> str:
    return str(uuid.uuid4().hex[:20])

def base_64_encoder_to_bytes(data: str) -> bytes:
    return base64.b64encode(data.encode())

def base_64_encoder(message:str)->str:
    return base_64_encoder_to_bytes(message).decode()


def encode_cips_message(cips_message: str) -> str: ...


def encode_esewa_message(message: str, secret) -> str:
    hmac_256 = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    digest = hmac_256.digest()
    signature = base64.b64encode(digest).decode("utf-8")
    return signature


def decode_esewa_message(message) -> str:
    """eSewa will send encoded message like this:
    eyJ0cmFuc2FjdGlvbl9jb2RlIjoiMExENUNFSCIsInN0YXR1cyI6IkNPTVBMRVRFI
    iwidG90YWxfYW1vdW50IjoiMSwwMDAuMCIsInRyYW5zYWN0aW9uX3V1aWQiOiIyNDA
    2MTMtMTM0MjMxIiwicHJvZHVjdF9jb2RlIjoiTlAtRVMtQUJISVNIRUstRVBBWSI
    sInNpZ25lZF9maWVsZF9uYW1lcyI6InRyYW5zYWN0aW9uX2NvZGUsc3RhdHVzLHR
    vdGFsX2Ftb3VudCx0cmFuc2FjdGlvbl91dWlkLHByb2R1Y3RfY29kZSxzaWduZWRfZ
    mllbGRfbmFtZXMiLCJzaWduYXR1cmUiOiJNcHd5MFRGbEhxcEpqRlVER2ljKzIybWR
    vZW5JVFQrQ2N6MUxDNjFxTUFjPSJ9

    We need to decode this message. This function handles decoding the message and returns
     """
    decoded_message = base64.b64decode(message)
    return decoded_message.decode()


def sign_connect_ips_message(cips_message: str, certificate_path, certificate_password) -> bytes:
    with open(certificate_path, "rb") as cert_file:
        cert_data = cert_file.read()

    # now load the pfx data
    private_key, certificate_data, _ = pkcs12.load_key_and_certificates(
        data=cert_data,
        password=certificate_password,
    )
    print("Private key:", private_key)
    print("Certificate data:", certificate_data)
    message_encoded = base_64_encoder_to_bytes(cips_message)

    signature = private_key.sign(
        data=message_encoded,
    )
    return signature


def decode_imepay_message(message:str):
    try:
        decoded_str = base64.b64decode(message).decode()
        return decoded_str
    except binascii.Error:
        return None


def prepare_imepay_header(**kwargs):
    username = kwargs.get("username")
    password = kwargs.get("password")
    merchant_module = kwargs.get("merchant_module")
    auth = f"{username}:{password}"
    auth_encoded = base_64_encoder(auth)
    module_encoded = base_64_encoder(merchant_module)

    return {
        "Content-Type": "application/json",
        "Authorization": auth_encoded,
        "Module": module_encoded,
    }


def prepare_imepay_initiate_payload(**kwargs):
    obj = kwargs.get("obj")
    merchant_code = kwargs.get("merchant_code")
    payload = {
        "MerchantCode": merchant_code,
        "Amount": obj.amount,
        "RefId": obj.transaction_id,
    }
    return payload


@retry_request(max_retries=3, initial_delay=2)
def payment_request_with_retry(method, url, data, headers=None, auth=None):
    if auth:
        response, status = requests.request(method, url, data=data, auth=auth)
        return response, status
    response, status = requests.request(method, url, data=data, headers=headers)
    return response, status
