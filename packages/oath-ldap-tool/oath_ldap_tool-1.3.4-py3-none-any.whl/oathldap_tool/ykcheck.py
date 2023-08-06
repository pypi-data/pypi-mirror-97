# -*- coding: utf-8 -*-
"""
oathldap_tool.ykadd -- sub-command for adding LDAP entry for Yubikey token
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

# from python-usb package
from usb.core import USBError

# from ldap0 package
from ldap0 import LDAPError

# from oathldap_tool package
from .yubikey import YubiKeySearchError
from . import (
    SEP_LINE,
    ErrorExit,
    cli_output,
    display_owner,
)
from .base import wait_for_yubikey
from .ldap import OathLDAPConn, OWNER_PERSON_ATTRS

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def ykcheck_once(args, oath_ldap):
    """
    Adds Yubikey token entry to OATH-LDAP server
    """
    try:

        yk_device = wait_for_yubikey()

        token_dn = oath_ldap.get_token_dn(args.ldap_url.dn, yk_device.serial)
        token = oath_ldap.read_s(
            token_dn,
            attrlist=[args.owner_attr],
        )
        cli_output('Token entry found: {0}'.format(token_dn))

        owner = oath_ldap.read_s(
            token.entry_s[args.owner_attr][0],
            attrlist=OWNER_PERSON_ATTRS,
        )
        display_owner(owner, OWNER_PERSON_ATTRS)

        if yk_device.enabled_slots:
            otp_value = input('Push button to generate OTP value --> ').strip()
            # send compare request to OATH-LDAP server
            otp_result = oath_ldap.compare_s(token_dn, 'oathHOTPValue', otp_value.encode('utf-8'))
            cli_output('Check result: {0}'.format(otp_result))
        else:
            cli_output('No check because no slots enabled.')

    except (
            USBError,
            LDAPError,
            ErrorExit,
            YubiKeySearchError,
        ) as err:
        cli_output(str(err), lf_after=2)

    # end of ykcheck_once()


def ykcheck(args):
    """
    Entry point for sub-command ykcheck
    """

    oath_ldap = OathLDAPConn.admin_connect(args.ldap_url, args.admin_dn)

    while True:
        ykcheck_once(args, oath_ldap)
        cli_output(SEP_LINE, lf_before=0, lf_after=1)
        if args.continuous:
            input('Hit [RETURN] key to continue with another Yubikey device...')
        else:
            break

    # end of ykcheck()
