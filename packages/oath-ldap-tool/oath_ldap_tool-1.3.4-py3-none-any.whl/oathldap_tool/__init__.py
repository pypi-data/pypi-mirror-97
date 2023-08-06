# -*- coding: utf-8 -*-
"""
oathldap -- Python package for OATH-LDAP client tool
"""

import sys
import getpass

import ldap0
import ldap0.base
from ldap0 import LDAPError
from ldap0.ldapurl import LDAPUrl
from ldap0.ldapobject import ReconnectLDAPObject

__all__ = [
    'cli_output',
    'ABORT_MSG_EXIT',
    'ABORT_MSG_RETRY',
    'ErrorExit',
    'SEP_LINE',
]

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

SEP_LINE = 80 * '-'

ABORT_MSG_EXIT = 'Aborted -> exit'
ABORT_MSG_RETRY = 'Aborted -> please insert new Yubikey'

#---------------------------------------------------------------------------
# Classes
#---------------------------------------------------------------------------

class ErrorExit(Exception):
    """
    to be raised if any condition should result in program exit
    """

    def __init__(self, msg: str, code: int = 1):
        Exception.__init__(self, msg)
        self.code = code

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def cli_output(text: str, lf_before: int = 1, lf_after: int = 1):
    """
    Command-line program output
    """
    sys.stdout.write(''.join((
        lf_before*'\n',
        text,
        lf_after*'\n',
    )))


def display_owner(owner, attrs):
    """
    Command-line output of token owner attributes
    """
    cli_output('Found owner entry: {0}'.format(owner.dn_s), lf_before=1)
    for attr in attrs:
        if attr in owner.entry_s:
            cli_output('{0}: {1}'.format(attr, owner.entry_s[attr][0]), lf_before=0, lf_after=1)
