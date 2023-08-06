# -*- coding: utf-8 -*-
"""
oathldap_tool.ykadd -- sub-command for generating OATH-LDAP primary key pair
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

import time
import os

# from jwcrypto package
from jwcrypto.jwk import JWK

# from oathldap_tool package
from . import cli_output

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

KEY_TYPE = 'RSA'

KEYID_FORMAT = 'oathldap_primary_key_{0}'

# default permissions for the generated files
KEY_PRIV_PERMS = 0o0600
KEY_PUB_PERMS = 0o0644

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def genkey(args):
    """
    generate new RSA key pair for encrypted shared secrets
    """

    key_id = KEYID_FORMAT.format(
        time.strftime('%Y%m%d%H%M', time.gmtime(time.time()))
    )

    privkey_filename = os.path.join(args.key_path, key_id+'.priv')
    pubkey_filename = os.path.join(args.key_path, key_id+'.pub')

    cli_output('Generating RSA-{0:d} key pair...'.format(args.key_size), lf_before=0)
    key = JWK(
        kty=KEY_TYPE,
        use='enc',
        generate=KEY_TYPE,
        kid=key_id,
        size=args.key_size,
    )

    with open(privkey_filename, 'w', encoding='utf-8') as fileobj:
        fileobj.write(key.export())
    os.chmod(privkey_filename, KEY_PRIV_PERMS)
    cli_output('wrote {0}'.format(privkey_filename, lf_before=0))

    with open(pubkey_filename, 'w', encoding='utf-8') as fileobj:
        fileobj.write(key.export_public())
    os.chmod(pubkey_filename, KEY_PUB_PERMS)
    cli_output('wrote {0}'.format(pubkey_filename), lf_before=0)

    # end of genkey()
