# -*- coding: utf-8 -*-
"""
oathldap_tool.ykinit -- sub-command for displaying Yubikey token information
"""

#---------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------

# from python-usb package
from usb.core import USBError

# from oathldap_tool package
from .yubikey import YubiKeySearchError, YKTokenDevice
from . import ErrorExit, cli_output

#---------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------

def ykinfo(args):
    """
    Entry point for sub-command ykinfo

    Shows information about connected Yubikey device.
    """
    try:
        yk_device = YKTokenDevice.search()
        cli_output(yk_device.info_msg(), lf_before=0, lf_after=1)
    except (
            ErrorExit,
            USBError,
            YubiKeySearchError,
        ) as err:
        cli_output(str(err))
    # end of ykinfo()
