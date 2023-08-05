import rsa
import base64
import typing

from Crypto.PublicKey import RSA
from .strutils import smart_get_binary_data


def newkeys(nbits=2048):
    sk = RSA.generate(nbits)
    pk = sk.publickey()
    return pk, sk

def load_private_key(text, passphrase=None):
    sk = RSA.import_key(text, passphrase=passphrase)
    return sk

def load_public_key(text):
    pk = RSA.import_key(text)
    return pk

def load_public_key_from_private_key(text, passphrase=None):
    sk = load_private_key(text, passphrase)
    pk = sk.publickey()
    return pk

def encrypt(data: bytes, pk: typing.Union[RSA.RsaKey, rsa.PublicKey]):
    if isinstance(data, str):
        data = data.encode("utf-8")
    if isinstance(pk, RSA.RsaKey):
        pk = rsa.PublicKey(pk.n, pk.e)
    encrypted_data = rsa.encrypt(data, pk)
    return "".join(base64.encodebytes(encrypted_data).decode().splitlines())

def decrypt(data: str, sk: typing.Union[RSA.RsaKey, rsa.PrivateKey]):
    if isinstance(sk, RSA.RsaKey):
        sk = rsa.PrivateKey(sk.n, sk.e, sk.d, sk.p, sk.q)
    encrypted_data = smart_get_binary_data(data)
    data = rsa.decrypt(encrypted_data, sk)
    return data

def export_key(rsakey: typing.Union[RSA.RsaKey, rsa.PublicKey, rsa.PrivateKey]):
    if isinstance(rsakey, rsa.PublicKey):
        rsakey = RSA.RsaKey(n=rsakey.n, e=rsakey.e)
    elif isinstance(rsakey, rsa.PrivateKey):
        rsakey = RSA.RsaKey(n=rsakey.n, e=rsakey.e, d=rsakey.d, p=rsakey.p, q=rsakey.q)
    return rsakey.export_key().decode()
