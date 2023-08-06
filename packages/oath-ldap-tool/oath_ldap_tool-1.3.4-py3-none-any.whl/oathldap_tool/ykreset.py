# -*- coding: utf-8 -*-
"""
oathldap_tool.ykreset -- sub-command for clearing Yubikey tokens
"""

import time

from yubico.yubikey_usb_hid import YubiKeyUSBHIDError

# from oathldap package
from . import (
    ABORT_MSG_RETRY,
    SEP_LINE,
    cli_output,
    ErrorExit,
)
from .base import (
    ask_access_code,
    access_code_seq,
    wait_for_yubikey,
)


def ykreset_once(args, verbose=False, force=False) -> int:
    """
    clear one device, returns serial no. of  device
    """

    yk_device = wait_for_yubikey()

    # if there are enabled slots we need the currently valid device password
    if yk_device.enabled_slots:
        if args.continuous or not force:
            confirm_input = input(
                'Confirm with word "reset" to clear the device '
                'or remove Yubikey device and hit [ENTER] to rescan --> '
            )
            if confirm_input.lower() != 'reset':
                raise ErrorExit(ABORT_MSG_RETRY)
        if args.current_access_code:
            current_access_code = args.current_access_code
        else:
            current_access_code = ask_access_code()
        brute_force = current_access_code.count('*') == 1
        ac_seq = access_code_seq(aclen=6, code_pattern=current_access_code)
        ykreset_count = 0
        ykreset_start = time.time()
        ykreset_disp_time = 0.0
        for ac_try in ac_seq:
            ykreset_count += 1
            try:
                if verbose:
                    cli_output(
                        'Clearing slot(s) {0} with access code {1}...'.format(
                            yk_device.enabled_slots,
                            ac_try,
                        )
                    )
                for slot in yk_device.enabled_slots:
                    yk_device.reset_slot(slot, ac_try)
                yk_device.clear(ac_try)
            except YubiKeyUSBHIDError:
                ykreset_time = time.time() - ykreset_start
                if verbose or ykreset_time - ykreset_disp_time >= 10.0:
                    cli_output(
                        'Failed {0:d} attempts after {1:f} secs'.format(
                            ykreset_count,
                            ykreset_time,
                        ),
                        lf_before=1,
                        lf_after=1,
                    )
                    ykreset_disp_time = ykreset_time
            else:
                ykreset_time = time.time() - ykreset_start
                cli_output(
                    'Successfully cleared slot(s) with access code {0}'.format(ac_try),
                    lf_before=1,
                    lf_after=1,
                )
                if brute_force:
                    cli_output(
                        'Needed {0:d} attempts in {1:f} secs'.format(
                            ykreset_count,
                            ykreset_time,
                        ),
                        lf_before=0,
                        lf_after=1,
                    )
                break
        else:
            cli_output('Could not clear slot(s) with access code {0}'.format(current_access_code))
    else:
        cli_output('No slot(s), nothing to clear')

    return yk_device.serial


def ykreset(args):
    """
    Clears (multiple) Yubikey tokens
    """
    while True:
        ykreset_once(args, args.verbose, args.force)
        cli_output(SEP_LINE, lf_before=0, lf_after=1)
        if args.continuous:
            input('Hit [RETURN] key to continue with another Yubikey device...')
        else:
            break
    # end of ykreset()
