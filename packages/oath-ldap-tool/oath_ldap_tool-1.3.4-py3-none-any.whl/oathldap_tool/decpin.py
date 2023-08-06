# -*- coding: utf-8 -*-
"""
oathldap_tool.decpin -- sub-command for extracting decrypted PIN from token entry
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

import os
import json
import glob

# from jwcrypto
try:
    from jwcrypto.jwk import JWK
    from jwcrypto.jwe import JWE
except ImportError:
    JWE = JWK = None

# from ldap0 package
import ldap0
import ldap0.filter
from ldap0 import LDAPError

# from oathldap_tool package
from . import SEP_LINE, ErrorExit, cli_output
from .ldap import OathLDAPConn

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

TOKEN_FILTER_TMPL = (
    '(&'
      '(objectClass=oathToken)'
      '(oathTokenPIN=*)'
      '(|'
        '(serialNumber={0})'
        '(oathTokenIdentifier={0})'
        '(oathTokenSerialNumber={0})'
      ')'
    ')'
)

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------


def _load_key(key_path, key_id):
    """
    Load JWE keys defined by globbing pattern in :key_files:
    """
    for private_key_filename in glob.glob(os.path.join(key_path, '*.priv')):
        with open(private_key_filename, 'rb') as key_file:
            privkey_json = key_file.read()
        private_key = JWK(**json.loads(privkey_json))
        if key_id == private_key.key_id:
            break
    else:
        raise ErrorExit('No private key with key id %r' % (key_id,))
    return private_key
    # end of _load_keys()


def _decrypt_pin(key_path, oath_pin):
    """
    This methods extracts and decrypts the token's OATH shared
    secret from the token's LDAP entry given in argument
    :token_entry:
    """
    if not JWE:
        raise ErrorExit('Package jwcrypto not installed')
    json_s = json.loads(oath_pin)
    key_id = json_s['header']['kid']
    jwe_decrypter = JWE()
    primary_key = _load_key(key_path, key_id)
    jwe_decrypter.deserialize(oath_pin, primary_key)
    return jwe_decrypter.plaintext



def decpin(args):
    """
    Entry point for sub-command decpin

    Retrieves and decrypts PIN from token entry in OATH-LDAP server
    """
    try:

        # Open OATH-LDAP connection interactively asking for admin password
        oath_ldap = OathLDAPConn.admin_connect(args.ldap_url, args.admin_dn)

        # search for OATH token entry
        token_filter = TOKEN_FILTER_TMPL.format(ldap0.filter.escape_str(args.token_id))
        token = oath_ldap.find_unique_entry(
            args.ldap_url.dn,
            args.ldap_url.scope or ldap0.SCOPE_SUBTREE,
            token_filter,
            attrlist=['oathTokenPIN'],
        )

        # close LDAP connection
        oath_ldap.unbind_s()

        cli_output('Found token entry {0!r}'.format(token.dn_s), lf_before=0)
        cli_output(
            'Decrypted PIN: {0}'.format(
                _decrypt_pin(args.key_path, token.entry_as['oathTokenPIN'][0]).decode('utf-8')
            ),
            lf_after=1,
        )
        cli_output(SEP_LINE, lf_before=0, lf_after=1)


    except (LDAPError, ErrorExit) as err:
        cli_output(str(err))

    # end of decpin()
