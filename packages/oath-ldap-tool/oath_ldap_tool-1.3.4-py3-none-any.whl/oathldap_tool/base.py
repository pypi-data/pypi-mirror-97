# -*- coding: utf-8 -*-
"""
oathldap_tool.ykinit -- sub-command for initializing a Yubikey token
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

import sys
import json
import time

# from jwcrypto package
from jwcrypto.jwk import JWK
from jwcrypto.jwe import JWE

# from python-usb package
from usb.core import USBError

from .yubikey import YubiKeySearchError, YKTokenDevice
from . import cli_output

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

JWE_DEFAULT_ALG = 'RSA-OAEP'
JWE_DEFAULT_ENC = 'A256GCM'

# alphabet used for generating Yubikey access codes
# for avoiding similar looking characters
ACCESS_CODE_ALPHABET = 'abcdefghijkmnpqrstuvwxyz23456789'

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def jwk_read(key_filename: str) -> JWK:
    """
    reads a JWK public key from file and returns the JWK object
    """
    with open(key_filename, 'rb') as pubkey_file:
        pk_json = pubkey_file.read()
    return JWK(**json.loads(pk_json))


def jwe_encrypt(
        jwk_obj: JWK,
        plaintext: bytes,
        alg: str =JWE_DEFAULT_ALG,
        enc: str =JWE_DEFAULT_ENC,
    ) -> str:
    """
    returns JWE strings with :plaintext: being asymmetrically encrypted
    with public key read from file with filename :key_filename:
    """
    jwe_obj = JWE(plaintext=plaintext)
    jwe_obj.add_recipient(
        jwk_obj,
        header=json.dumps(dict(
            alg=alg,
            enc=enc,
            kid=jwk_obj.key_id,
        )),
    )
    return jwe_obj.serialize()


def access_code_seq(aclen=6, code_pattern='*'):
    """
    access codes sequence generator for brute-forcing
    """
    star_pos = code_pattern.find('*')
    if star_pos == -1:
        yield code_pattern
        return
    prefix = [code_pattern[0:star_pos]]
    suffix = [code_pattern[star_pos+1:]]
    aclen = aclen - len(prefix[0]) - len(suffix[0])
    alphabet_len = len(ACCESS_CODE_ALPHABET)
    for i in range(alphabet_len**aclen):
        yield ''.join(
            prefix+
            [
                ACCESS_CODE_ALPHABET[(i // (alphabet_len ** j)) % alphabet_len]
                for j in range(aclen)
            ]
            +suffix
        )


def ask_access_code() -> str:
    """
    interactively ask for current slot password repeately in case of input error
    """
    current_access_code = input('Provide old slot password --> ')
    while (
            current_access_code
            and current_access_code != '*'
            and not (len(current_access_code) == 6 and current_access_code.isalnum())
        ):
        current_access_code = input('Wrong format of slot password => try again')
    return current_access_code


def wait_for_yubikey() -> YKTokenDevice:
    """
    wait until user plugs in Yubikey device
    """
    try:
        yk_device = YKTokenDevice.search()
    except (YubiKeySearchError, USBError):
        cli_output('Waiting for single Yubikey device.', lf_before=1)
        while True:
            try:
                yk_device = YKTokenDevice.search()
            except (YubiKeySearchError, USBError):
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(0.8)
            else:
                break
    cli_output('Found Yubikey device no. {serial}'.format(serial=yk_device.serial), lf_before=2)
    cli_output(yk_device.info_msg(), lf_before=0)
    return yk_device
