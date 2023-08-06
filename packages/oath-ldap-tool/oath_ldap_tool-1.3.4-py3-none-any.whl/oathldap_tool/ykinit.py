# -*- coding: utf-8 -*-
"""
oathldap_tool.ykinit -- sub-command for initializing Yubikey tokens
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

import time
import sys
import secrets

# from python-usb package
from usb.core import USBError

# from ldap0 package
from ldap0 import LDAPError
from ldap0.pw import random_string

# from oathldap package
from .yubikey import YubiKeySearchError, YKTokenDevice
from . import (
    cli_output,
    ErrorExit,
    SEP_LINE,
)
from .base import (
    ACCESS_CODE_ALPHABET,
    jwe_encrypt,
    jwk_read,
)
from .ykreset import ykreset_once
from .ldap import OathLDAPConn

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def ykinit_once(args, jwk_obj, oath_ldap):
    """
    Run as stand-alone script
    """

    try:

        access_code = args.access_code or random_string(ACCESS_CODE_ALPHABET, 6)
        if len(access_code) != 6 or not access_code.isalnum():
            raise ErrorExit(
                'New slot password must be exactly six (6) alpha-numeric ASCII characters!'
            )

        # save for later check to prevent user from accidently changing device
        yk_serial = ykreset_once(args)

        clear_time = time.time()

        if args.admin_dn:
            token_dn = oath_ldap.get_token_dn(args.ldap_url.dn, yk_serial)
            oath_ldap.reset_token(token_dn)
        else:
            # Open OATH-LDAP connection interactively asking for
            # enrollment password for this particular device
            oath_ldap = OathLDAPConn.token_connect(args.ldap_url, yk_serial)
            token_dn = oath_ldap.get_whoami_dn()

        # get some init parameters from OATH-LDAP
        oath_identifier, _, otp_length, oath_enckey = oath_ldap.get_hotp_params(token_dn)
        if oath_enckey is None:
            oath_enckey = jwk_obj

        if oath_enckey is None:
            raise ErrorExit('No public key available to encrypt shared secret!')

        cli_output('Key used for encrypting secrets:')
        cli_output(
            'kid: {kid}\nthumbprint: {thumbprint}'.format(
                kid=oath_enckey.key_id,
                thumbprint=oath_enckey.thumbprint()
            ),
            lf_before=0,
        )

        # generate new shared secret (OTP seed)
        oath_secret = secrets.token_bytes(20)

        # write new encrypted shared secret and
        # new encrypted device password into OATH-LDAP token entry
        oath_ldap.update_token(
            token_dn,
            jwe_encrypt(oath_enckey, oath_secret),
            jwe_encrypt(oath_enckey, access_code),
        )
        cli_output('Updated secret in OATH-LDAP entry {0!r}'.format(token_dn))
        oath_ldap.unbind_s()

        # wait some for the cleared device time if still needed
        sleep_time = 5.0 - (time.time() - clear_time)
        if sleep_time >= 0.0:
            cli_output('Waiting {0:0.1f} secs until Yubikey reconnect...'.format(sleep_time))
            time.sleep(sleep_time)

        # Search the device again
        yk_device = YKTokenDevice.search()
        if yk_serial != yk_device.serial:
            # better safe than sorry!
            raise ErrorExit('Device serial no. changed!')

        # now finally initialize the device
        cli_output(
            (
                '*** Write down new password (access code) for Yubikey {serial} '
                'and keep in a safe place -> {accesscode} ***'
            ).format(
                serial=yk_device.serial,
                accesscode=access_code,
            ),
            lf_before=2,
            lf_after=2,
        )
        cli_output('Initializing Yubikey device no. {0}...'.format(yk_device.serial))
        yk_device.initialize(
            oath_secret,
            otp_length,
            oath_identifier,
            access_code,
        )

    except (
            LDAPError,
            USBError,
            YubiKeySearchError,
        ) as err:
        cli_output(str(err))

    else:
        cli_output('Yubikey successfully initialized. Unplug it right now!', lf_after=2)

    # end of ykinit_once()


def ykinit(args):
    """
    Entry point for sub-command ykinit

    Initializes (multiple) Yubikey tokens for HOTP and sends encrypted shared secret
    to OATH-LDAP server after authenticating as the token entry with the
    enrollment password
    """

    if args.pubkey:
        cli_output('Read JWK public key file {0}'.format(args.pubkey))
        try:
            jwk_obj = jwk_read(args.pubkey)
        except IOError as err:
            cli_output('Error reading JWK public key file {0} -> {1!r}'.format(args.pubkey, err))
            sys.exit(1)
        cli_output('kid: {kid}\nthumbprint: {thumbprint}'.format(
            kid=jwk_obj.key_id,
            thumbprint=jwk_obj.thumbprint()),
            lf_before=0
        )
    else:
        jwk_obj = None

    if args.admin_dn:
        oath_ldap = OathLDAPConn.admin_connect(args.ldap_url, args.admin_dn)
    else:
        oath_ldap = None

    while True:
        ykinit_once(args, jwk_obj, oath_ldap)
        cli_output(SEP_LINE, lf_before=0, lf_after=1)
        if args.continuous:
            input('Hit [RETURN] key to continue with another Yubikey device...')
        else:
            break

    # end of ykinit()
