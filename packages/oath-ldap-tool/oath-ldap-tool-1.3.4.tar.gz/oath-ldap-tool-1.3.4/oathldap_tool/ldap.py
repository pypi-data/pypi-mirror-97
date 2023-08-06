# -*- coding: utf-8 -*-
"""
oathldap_tool.ykinit -- sub-command for initializing a Yubikey token
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

import time
import getpass
import json
from typing import Optional, Tuple

# from jwcrypto package
from jwcrypto.jwk import JWK

# from ldap0 package
import ldap0
from ldap0.ldapurl import LDAPUrl
from ldap0.ldapobject import ReconnectLDAPObject

from . import (
    ABORT_MSG_EXIT,
    ABORT_MSG_RETRY,
    SEP_LINE,
    ErrorExit,
    cli_output,
)

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

LDAP_TIMEOUT = 15.0

# Cache TTL used when reading oathParams entries
OATH_PARAMS_CACHE_TTL = 1800.0

# string template for bind-DN of an oathToken entry
OATH_TOKEN_BINDDN_TMPL = 'serialNumber=yubikey-{unique_id},{search_base}'

# attributes useful to display ownership
OWNER_PERSON_ATTRS = ['displayName', 'employeeNumber', 'uniqueIdentifier', 'mail']

# LDAP filter template for searching owner entries
OWNER_FILTER_TMPL = (
    '(&'
      '(objectClass=inetOrgPerson)'
      '(|'
        '(entryDN={0})'
        '(entryUUID={0})'
        '(uid={0})'
        '(mail={0})'
        '(uniqueIdentifier={0})'
        '(employeeNumber={0})'
      ')'
    ')'
)

OATH_TOKEN_RESET_ATTRS = [
    'oathHOTPCounter',
    'oathLastLogin',
    'oathFailureCount',
    'oathLastFailure',
]

#---------------------------------------------------------------------------
# Classes
#---------------------------------------------------------------------------

class OathLDAPConn(ReconnectLDAPObject):
    """
    OATH-LDAP connection
    """

    def __init__(self, ldap_uri, who=None, cred=None, **kwargs):
        ReconnectLDAPObject.__init__(self, ldap_uri, **kwargs)
        self.set_option(ldap0.OPT_NETWORK_TIMEOUT, LDAP_TIMEOUT)
        if who:
            self.simple_bind_s(who, cred)

    @classmethod
    def admin_connect(cls, ldap_url: LDAPUrl, ldap_who: str):
        """
        returns OathLDAPConn connected as token specified by :serial: after
        interactively asking the user for the two enrollment password parts
        """
        ldap_uri = ldap_url.connect_uri()
        if (
                ldap_url.urlscheme.lower() == 'ldapi'
                and ldap_who is None
            ):
            oath_ldap = cls(ldap_uri)
            oath_ldap.sasl_non_interactive_bind_s('EXTERNAL')
            return oath_ldap
        while True:
            ldap_pw = getpass.getpass('\nEnter password for admin %r' % ldap_who)
            if not ldap_pw:
                raise ErrorExit(ABORT_MSG_EXIT)
            try:
                oath_ldap = cls(ldap_uri)
                oath_ldap.simple_bind_s(ldap_who, ldap_pw)
            except ldap0.INVALID_CREDENTIALS:
                cli_output('Password(s) wrong => try again')
            else:
                break
        input('Remove Yubikey used for login, press [ENTER] to continue...')
        cli_output(SEP_LINE, lf_before=1, lf_after=2)
        return oath_ldap

    @classmethod
    def token_connect(cls, ldap_url: LDAPUrl, serial: str):
        """
        returns OathLDAPConn connected as token specified by :serial: after
        interactively asking the user for the two enrollment password parts
        """
        ldap_who = OATH_TOKEN_BINDDN_TMPL.format(
            unique_id=serial,
            search_base=ldap_url.dn
        )
        while True:
            cli_output(
                (
                    'Enter both enrollment password parts for Yubikey no. %s '
                    'or remove YubiKey device and hit [ENTER] to rescan'
                    '\nLDAP-DN: %r'
                ) % (serial, ldap_who)
            )
            ldap_initpw1 = input("Part #1 --> ")
            if not ldap_initpw1:
                raise ErrorExit(ABORT_MSG_RETRY)
            ldap_initpw2 = input("Part #2 --> ")
            if not ldap_initpw2:
                raise ErrorExit(ABORT_MSG_RETRY)
            try:
                oath_ldap = cls(
                    ldap_url.connect_uri(),
                    ldap_who,
                    ldap_initpw1+ldap_initpw2,
                )
            except ldap0.INVALID_CREDENTIALS:
                cli_output('Enrollment password(s) wrong => try again')
            else:
                break
        return oath_ldap

    def get_token_dn(self, search_base, yk_serial):
        """
        search token entry by serial
        """
        return OATH_TOKEN_BINDDN_TMPL.format(
            unique_id=yk_serial,
            search_base=search_base
        )

    def get_hotp_params(self, token_dn) -> Tuple[str, str, int, Optional[JWK]]:
        """
        read some HOTP parameters from token and policy entries
        """
        token = self.read_s(
            token_dn,
            filterstr='(objectClass=oathHOTPToken)',
            attrlist=[
                'oathHOTPParams',
                'oathTokenIdentifier',
            ],
        )
        token_params = self.read_s(
            token.entry_s['oathHOTPParams'][0],
            filterstr='(objectClass=oathHOTPParams)',
            attrlist=[
                'oathEncKey',
                'oathHMACAlgorithm',
                'oathOTPLength',
            ],
            cache_ttl=OATH_PARAMS_CACHE_TTL,
        )
        if 'oathEncKey' in token_params.entry_s:
            enc_key = JWK(**json.loads(token_params.entry_s['oathEncKey'][0]))
        else:
            enc_key = None
        return (
            token.entry_s.get('oathTokenIdentifier', [''])[0],
            token_params.entry_s['oathHMACAlgorithm'][0],
            int(token_params.entry_s['oathOTPLength'][0]),
            enc_key,
        )

    def reset_token(self, token_dn):
        """
        reset token entry
        """
        token = self.read_s(token_dn, attrlist=OATH_TOKEN_RESET_ATTRS)
        token_mods = [
            (
                ldap0.MOD_REPLACE,
                b'oathSecretTime',
                [time.strftime('%Y%m%d%H%M%SZ', time.gmtime(time.time())).encode('ascii')],
            ),
        ]
        token_mods.extend([
            (ldap0.MOD_DELETE, del_attr.encode('ascii'), None)
            for del_attr in OATH_TOKEN_RESET_ATTRS
            if del_attr in token.entry_s
        ])
        self.modify_s(token_dn, token_mods)
        try:
            self.modify_s(token_dn, [(ldap0.MOD_DELETE, b'oathSecret', None)])
        except ldap0.NO_SUCH_ATTRIBUTE:
            pass
        # end of reset_token()

    def update_token(self, token_dn, otp_secret, token_pin):
        """
        Write OATH-LDAP attributes, especially the already encrypted
        :otp_secret:, to the OATH-LDAP token entry this connection is bound as.
        """
        # Actually send LDAP modify request
        self.modify_s(
            token_dn or self.get_whoami_dn(),
            [
                (ldap0.MOD_ADD, b'oathHOTPCounter', [b'0']),
                (ldap0.MOD_REPLACE, b'oathTokenPIN', [token_pin.encode('utf-8')]),
                (ldap0.MOD_ADD, b'oathSecret', [otp_secret.encode('utf-8')]),
            ],
        )
        # end of update_token()
