import base64
import binascii
import uuid, hmac, hashlib
import requests

from utils.decorators_ import retry_request


def generate_transaction_id() -> str:
    return str(uuid.uuid4().hex[:20])

def base_64_encoder(message:str)->str:
    return base64.b64encode(message.encode()).decode()


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


def sign_connect_ips_message(cips_message: bytes, certificate_path) -> str:
    with open(certificate_path, "rb") as cert_file:
        cert_data = cert_file.read()


def get_encoded_token_cips(token: str, cert_path) -> str:
    message = token.encode()
    signed_message = sign_connect_ips_message(message, cert_path)
    return signed_message


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
def ime_pay_request_with_retry(method, url, data, headers):
    response, status = requests.request(method, url, data=data, headers=headers)
    return response, status
