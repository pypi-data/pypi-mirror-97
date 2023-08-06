# -*- coding: utf-8 -*-
"""
OATH-LDAP command-line tool
"""

import sys
import os
import argparse

import ldap0
from ldap0.ldapurl import LDAPUrl

# import the sub-command functions from other modules
from . import ErrorExit, cli_output, SEP_LINE
from .__about__ import __version__
from .decpin import decpin as cli_decpin
from .genkey import genkey as cli_genkey
from .ykadd import ykadd as cli_ykadd
from .ykcheck import ykcheck as cli_ykcheck
from .ykinfo import ykinfo as cli_ykinfo
from .ykinit import ykinit as cli_ykinit
from .ykreset import ykreset as cli_ykreset

__all__ = [
    'main',
    'cli_args',
]

#---------------------------------------------------------------------------
# Action classes
#---------------------------------------------------------------------------

class SetCACert(argparse.Action):
    """
    Argument parser action class for -C / --ca-certs
    """

    def __call__(self, parser, namespace, values, option_string=None):
        ldap0.set_option(ldap0.OPT_X_TLS_CACERTFILE, values.encode('utf-8'))


#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def cli_args():
    """
    CLI arguments
    """
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        prog=script_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='OATH-LDAP tool',
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    #-----------------------------------------------------------------------
    # sub-command decpin
    parser_decpin = subparsers.add_parser(
        'decpin',
        help='sub-command decpin',
        description=cli_decpin.__doc__,
    )
    parser_decpin.add_argument(
        '-H', '--ldap-url',
        dest='ldap_url',
        help='OATH-LDAP server URL',
        type=LDAPUrl,
        required=True,
    )
    parser_decpin.add_argument(
        '-D', '--admin-dn',
        dest='admin_dn',
        help='bind-DN to use for admin login',
        required=False,
    )
    parser_decpin.add_argument(
        '-C', '--ca-certs',
        dest='ca_certs',
        help='File with trusted CA certificate(s)',
        action=SetCACert,
        required=False,
    )
    parser_decpin.add_argument(
        '-p', '--key-path',
        dest='key_path',
        help='path where key files are stored',
        required=True,
    )
    parser_decpin.add_argument(
        '-i', '--token-id',
        dest='token_id',
        help='token identifier in OATH-LDAP entry',
        type=str,
        required=True,
    )
    parser_decpin.set_defaults(func=cli_decpin)

    #-----------------------------------------------------------------------
    # sub-command genkey
    parser_genkey = subparsers.add_parser(
        'genkey',
        help='sub-command genkey',
        description=cli_genkey.__doc__,
    )
    parser_genkey.add_argument(
        '-p', '--key-path',
        dest='key_path',
        help='path where to store generated key pair files',
        required=True,
    )
    parser_genkey.add_argument(
        '-s', '--key-size',
        dest='key_size',
        default=2048,
        help='key size of RSA key pair',
        type=int,
        required=False,
    )
    parser_genkey.set_defaults(func=cli_genkey)

    #-----------------------------------------------------------------------
    # sub-command ykinfo
    parser_ykinfo = subparsers.add_parser(
        'ykinfo',
        help='sub-command ykinfo',
        description=cli_ykinfo.__doc__,
    )
    parser_ykinfo.set_defaults(func=cli_ykinfo)

    #-----------------------------------------------------------------------
    # sub-command ykadd
    parser_ykadd = subparsers.add_parser(
        'ykadd',
        help='sub-command ykadd',
        description=cli_ykadd.__doc__,
    )
    parser_ykadd.add_argument(
        '-H', '--ldap-url',
        dest='ldap_url',
        help='OATH-LDAP server URL incl. search parameters',
        type=LDAPUrl,
        required=True,
    )
    parser_ykadd.add_argument(
        '-D', '--admin-dn',
        dest='admin_dn',
        help='bind-DN to use for admin login',
        required=True,
    )
    parser_ykadd.add_argument(
        '-C', '--ca-certs',
        dest='ca_certs',
        help='File with trusted CA certificate(s)',
        action=SetCACert,
        required=False,
    )
    parser_ykadd.add_argument(
        '-o', '--owner',
        dest='person_id',
        help='unique name or identifier to search for owner entry',
        required=False,
    )
    parser_ykadd.add_argument(
        '-l', '--ldif-template',
        dest='ldif_template',
        default='',
        help='base DN to be used for token entry',
        required=True,
    )
    parser_ykadd.add_argument(
        '-s', '--serial',
        dest='serial_nr',
        help='serial number of new Yubikey token',
        type=int,
        required=False,
    )
    parser_ykadd.add_argument(
        '-u', '--url',
        dest='enroll_url',
        help='URL for accessing oathenroll web app',
        default='',
        required=False,
    )
    parser_ykadd.add_argument(
        '-c', '--continue',
        dest='continuous',
        default=False,
        action='store_true',
        help='Continuous operation mode'
    )
    parser_ykadd.set_defaults(func=cli_ykadd)

    #-----------------------------------------------------------------------
    # sub-command ykcheck
    parser_ykcheck = subparsers.add_parser(
        'ykcheck',
        help='sub-command ykcheck',
        description=cli_ykcheck.__doc__,
    )
    parser_ykcheck.add_argument(
        '-H', '--ldap-url',
        dest='ldap_url',
        help='OATH-LDAP server URL incl. search parameters',
        type=LDAPUrl,
        required=True,
    )
    parser_ykcheck.add_argument(
        '-D', '--admin-dn',
        dest='admin_dn',
        help='bind-DN to use for admin login',
        required=True,
    )
    parser_ykcheck.add_argument(
        '-C', '--ca-certs',
        dest='ca_certs',
        help='File with trusted CA certificate(s)',
        action=SetCACert,
        required=False,
    )
    parser_ykcheck.add_argument(
        '-o', '--owner',
        dest='owner_attr',
        help='Name of owner attribute',
        default='owner',
        required=False,
    )
    parser_ykcheck.add_argument(
        '-c', '--continue',
        dest='continuous',
        default=False,
        action='store_true',
        help='Continuous operation mode'
    )
    parser_ykcheck.set_defaults(func=cli_ykcheck)

    #-----------------------------------------------------------------------
    # sub-command ykinit
    parser_ykinit = subparsers.add_parser(
        'ykinit',
        help='sub-command ykinit',
        description=cli_ykinit.__doc__,
    )
    parser_ykinit.add_argument(
        '-H', '--ldap-url',
        dest='ldap_url',
        help='OATH-LDAP server URL',
        type=LDAPUrl,
        required=True,
    )
    parser_ykinit.add_argument(
        '-D', '--admin-dn',
        dest='admin_dn',
        help='bind-DN to use for admin login',
        required=False,
    )
    parser_ykinit.add_argument(
        '-C', '--ca-certs',
        dest='ca_certs',
        help='File with trusted CA certificate(s)',
        action=SetCACert,
        required=False,
    )
    parser_ykinit.add_argument(
        '-k', '--public-key',
        dest='pubkey',
        help='Public key file to encrypt Yubikey shared secrets',
        required=False,
    )
    parser_ykinit.add_argument(
        '-p', '--new-slot-password',
        dest='access_code',
        default='',
        help='New Yubikey device password'
    )
    parser_ykinit.add_argument(
        '-o', '--old-slot-password',
        dest='current_access_code',
        help='Currently valid Yubikey device password'
    )
    parser_ykinit.add_argument(
        '-c', '--continue',
        dest='continuous',
        default=False,
        action='store_true',
        help='Continuous operation mode'
    )
    parser_ykinit.set_defaults(func=cli_ykinit)

    #-----------------------------------------------------------------------
    # sub-command ykreset
    parser_ykreset = subparsers.add_parser(
        'ykreset',
        help='sub-command ykreset',
        description=cli_ykreset.__doc__,
    )
    parser_ykreset.add_argument(
        '-o', '--old-slot-password',
        dest='current_access_code',
        help='Currently valid Yubikey device password'
    )
    parser_ykreset.add_argument(
        '-c', '--continue',
        dest='continuous',
        default=False,
        action='store_true',
        help='Continuous operation mode'
    )
    parser_ykreset.add_argument(
        '-v', '--verbose',
        dest='verbose',
        default=False,
        action='store_true',
        help='Verbose output for each brute-force attempt'
    )
    parser_ykreset.add_argument(
        '-f', '--force',
        dest='force',
        default=False,
        action='store_true',
        help='Force reset in non-interactive mode'
    )
    parser_ykreset.set_defaults(func=cli_ykreset)

    return parser.parse_args()
    # end of cli_args()


def main():
    """
    the main entry point
    """
    args = cli_args()
    try:
        args.func
    except AttributeError:
        pass
    else:
        cli_output(SEP_LINE, lf_before=0, lf_after=0)
        cli_output('OATH-LDAP {0} v{1}'.format(args.func.__name__, __version__))
        cli_output(SEP_LINE, lf_before=0, lf_after=1)
        try:
            args.func(args)
        except ErrorExit as err:
            cli_output(str(err), lf_after=2)
        except KeyboardInterrupt:
            cli_output('Exiting...')
    # end of main()


if __name__ == "__main__":
    main()
