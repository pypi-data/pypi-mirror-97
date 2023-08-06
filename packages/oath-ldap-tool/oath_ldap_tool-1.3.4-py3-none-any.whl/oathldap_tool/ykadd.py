# -*- coding: utf-8 -*-
"""
oathldap_tool.ykadd -- sub-command for adding LDAP entry for Yubikey token
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

from urllib.parse import urlparse, urlencode
import webbrowser

# from python-usb package
from usb.core import USBError

# from ldap0 package
import ldap0
import ldap0.base
from ldap0 import LDAPError
from ldap0.ldif import LDIFParser
from ldap0.tmpl import TemplateEntry

# from oathldap_tool package
from .yubikey import YubiKeySearchError
from . import (
    SEP_LINE,
    ErrorExit,
    cli_output,
    display_owner,
)
from .base import wait_for_yubikey
from .ldap import OathLDAPConn, OWNER_FILTER_TMPL, OWNER_PERSON_ATTRS

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def read_ldif_template(filename):
    """
    read LDIF file and return parsed template entry
    """
    # read the LDIF template
    try:
        with open(filename, 'rb') as ldif_file:
            t_dn, t_entry = LDIFParser(ldif_file).list_entry_records()[0]
    except IOError as err:
        raise ErrorExit('Unable to read LDIF template: %s' % (err,)) from err
    return t_dn, t_entry


def ykadd_once(args, oath_ldap, t_dn, t_entry):
    """
    Adds Yubikey token entry to OATH-LDAP server
    """
    try:

        if args.person_id:
            person_id = args.person_id
        else:
            person_id = input('Provide identifier to search for owner entry --> ').strip()

        # search a single owner entry by given owner identifier
        owner_filter = OWNER_FILTER_TMPL.format(ldap0.filter.escape_str(person_id))
        if args.ldap_url.filterstr is not None:
            owner_filter = '(&{0}{1})'.format(args.ldap_url.filterstr, owner_filter)
        owner = oath_ldap.find_unique_entry(
            args.ldap_url.dn,
            args.ldap_url.scope or ldap0.SCOPE_SUBTREE,
            owner_filter,
            attrlist=OWNER_PERSON_ATTRS,
        )
        display_owner(owner, OWNER_PERSON_ATTRS)

        if args.serial_nr:
            yk_serial = int(args.serial_nr)
        else:
            yk_device = wait_for_yubikey()
            yk_serial = yk_device.serial

        token_dn, token_entry = TemplateEntry(
            t_dn.decode('utf-8'),
            ldap0.base.decode_entry_dict(t_entry),
        ).ldap_entry(
            dict(
                search_base=args.ldap_url.dn,
                owner=owner.dn_s,
                serial=yk_serial,
            )
        )
        token_dn = ','.join((token_dn, args.ldap_url.dn))

        # finally add OATH-LDAP token entry
        oath_ldap.add_s(token_dn, token_entry)
        cli_output('Added OATH-LDAP token entry {0!r}'.format(token_dn), lf_after=2)
        oath_ldap.unbind_s()

        if args.enroll_url:
            # make sure we got syntactically valid URL
            urlparse(args.enroll_url)
            webbrowser.open(
                '?'.join((
                    args.enroll_url,
                    urlencode((('serial', yk_serial),))
                )),
                new=1,
                autoraise=True,
            )


    except ldap0.ALREADY_EXISTS:
        cli_output('Entry {0!r} already exists!'.format(token_dn), lf_after=2)

    except (
            USBError,
            LDAPError,
            ErrorExit,
            YubiKeySearchError,
        ) as err:
        cli_output(str(err), lf_after=2)

    # end of ykadd_once()


def ykadd(args):
    """
    Entry point for sub-command ykadd
    """

    # fail if incompatible argument combinations were specified
    if args.serial_nr:
        if args.initialize:
            raise ErrorExit('Argument -i/--init not usable with option -s/--serial')
        if args.continuous:
            raise ErrorExit('Argument -c/--continue not usable with option -s/--serial')
    if args.person_id and args.continuous:
        raise ErrorExit('Argument -c/--continue not usable with option -o/--owner')

    t_dn, t_entry = read_ldif_template(args.ldif_template)

    oath_ldap = OathLDAPConn.admin_connect(args.ldap_url, args.admin_dn)

    while True:
        ykadd_once(args, oath_ldap, t_dn, t_entry)
        cli_output(SEP_LINE, lf_before=0, lf_after=1)
        if args.continuous:
            input('Hit [RETURN] key to continue with another Yubikey device...')
        else:
            break

    # end of ykadd()
