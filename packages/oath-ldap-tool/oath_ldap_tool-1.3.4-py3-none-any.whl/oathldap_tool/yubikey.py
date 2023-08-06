# -*- coding: utf-8 -*-
"""
oathldap_tool.yubikey -- low-level Yubikey stuff
"""

import time
from binascii import unhexlify

# from python-yubico package
import yubico.yubikey_defs
from yubico.yubikey_base import YubiKeyError
from yubico import find_yubikey
from yubico.yubikey_config import YubiKeyConfig
from yubico.yubikey_neo_usb_hid import YubiKeyNEO_NDEF, YubiKeyNEO_DEVICE_CONFIG


__all__ = [
    'YubiKeySearchError',
    'YKTokenDevice',
]


DEFAULT_TICKET_FLAGS = (
    ('APPEND_CR', False),
    ('PROTECT_CFG2', True),
)

DEFAULT_EXTENDED_FLAGS = (
    ('SERIAL_API_VISIBLE', True),
    ('ALLOW_UPDATE', False),
    ('FAST_TRIG', True),
)

class YubiKeySearchError(Exception):
    """
    to be raised if search for a single Yubikey device failed
    """


class YKTokenDevice:
    """
    a single slot of a Yubikey token
    """
    yk_scan_code = 'h:9284978b2c869291898c8a2c9a849691972c868f88849588871b2c87922c8c972c848a848c91'

    def __init__(self, key):
        self._ykdev = key

    @classmethod
    def search(cls, max_skip=6, debug=False):
        """
        init instance by searching for exactly one device
        """
        yk_devices = []
        skip = 0
        while True:
            try:
                yk_dev = find_yubikey(debug=debug, skip=skip)
            except YubiKeyError as yk_error:
                if yk_error.reason != 'No YubiKey found':
                    raise yk_error
                # check whether to proceed with search
                if skip >= max_skip:
                    break
            else:
                yk_devices.append(yk_dev)
            skip += 1
        if not yk_devices:
            raise YubiKeySearchError('No Yubikey devices found!')
        if len(yk_devices) > 1:
            raise YubiKeySearchError('More than one Yubikey found. Only one allowed!')
        return cls(yk_devices[0])

    @property
    def model(self):
        """
        returns model name
        """
        return self._ykdev.model

    @property
    def serial(self):
        """
        returns serial number
        """
        return self._ykdev.serial()

    @property
    def version(self):
        """
        returns firmware version
        """
        return self._ykdev.version()

    @property
    def status(self):
        """
        returns device status
        """
        return self._ykdev.status()

    @property
    def enabled_slots(self):
        """
        returns list of numbers of enabled/configured slots
        """
        return self._ykdev.status().valid_configs()

    def info_msg(self):
        """
        returns string with info about the device
        """
        return '{model} no. {serial} {version} // Enabled slots: {slots}'.format(
            model=self.model,
            serial=self.serial,
            version=self.version,
            slots=', '.join(map(str, self.enabled_slots)) or 'none',
        )

    def _write_cfg(self, ykcfg, slot):
        """
        write mode-specific Yubikey configuration given in :cfg: to :slot:
        """
        if isinstance(ykcfg, YubiKeyConfig):
            self._ykdev.write_config(ykcfg, slot)
        elif isinstance(ykcfg, YubiKeyNEO_NDEF):
            self._ykdev.write_ndef(ykcfg, slot)
        elif isinstance(ykcfg, YubiKeyNEO_DEVICE_CONFIG):
            self._ykdev.write_device_config(ykcfg)
        else:
            raise TypeError('Unknown config type: {0!r}'.format(ykcfg))
        # end of _write_cfg()

    def init_hotp(
            self,
            slot,
            oath_secret,
            otp_len,
            oath_tokenid,
            access_code,
            ticket_flags=DEFAULT_TICKET_FLAGS,
            extended_flags=DEFAULT_EXTENDED_FLAGS,
        ):
        """
        Initialize a device slot for HOTP
        """
        # initialize HOTP in slot
        self._write_cfg(
            self._ykdev.init_device_config(mode=yubico.yubikey_defs.MODE.OTP),
            slot,
        )
        cfg = self._ykdev.init_config()
        if oath_tokenid:
            if not oath_tokenid.startswith('ubhe'):
                raise ValueError(
                    'Expected oath_tokenid with prefix "ubhe", but was %r' % (oath_tokenid)
                )
            cfg.mode_oath_hotp(
                secret=oath_secret,
                digits=otp_len,
                omp=0xe1,
                tt=0x63,
                mui=b'h:'+oath_tokenid[4:].encode('ascii'),
            )
            cfg.config_flag('OATH_FIXED_MODHEX2', True)
        else:
            cfg.mode_oath_hotp(secret=oath_secret, digits=otp_len)
        cfg.access_key(access_code.encode('ascii'))
        for flag_name, flag_val in ticket_flags:
            cfg.ticket_flag(flag_name, flag_val)
        for flag_name, flag_val in extended_flags:
            cfg.extended_flag(flag_name, flag_val)
        self._write_cfg(cfg, slot)
        # end of init_hotp()

    def is_enabled(self, slot):
        """
        check wether slot is already enabled/configured
        """
        return slot in self._ykdev.status().valid_configs()

    def _write_scancode(self, scancode, slot, access_code, current_access_code):
        # Check scancode argument
        if (
                not scancode.startswith('h:')
                or scancode == 'h:'
                or len(scancode) > 78
                or (len(scancode) % 2) != 0
            ):
            raise ValueError('Invalid scancode: %r' % (scancode,))
        scancode = scancode[2:]
        cfg = self._ykdev.init_config()
        cfg.enable_extended_scan_code_mode()
        if len(scancode) > 32:
            cfg.fixed_string('h:'+scancode[:32])
            scancode = scancode[32:]
        elif scancode:
            cfg.fixed_string('h:'+scancode)
            scancode = ''
        if len(scancode) > 12:
            cfg.uid = unhexlify(scancode[:12])
            scancode = scancode[12:]
        elif scancode:
            cfg.uid = unhexlify(scancode)
            scancode = ''
        if len(scancode) > 32:
            cfg.aes_key('h:'+scancode[:32])
            scancode = scancode[32:]
        elif scancode:
            cfg.aes_key('h:'+scancode.ljust(32, '0'))
            scancode = ''
        if self.is_enabled(slot) and current_access_code:
            cfg.unlock_key(current_access_code.encode('ascii'))
        cfg.extended_flag('SERIAL_API_VISIBLE', True)
        cfg.extended_flag('ALLOW_UPDATE', False)
        cfg.access_key(access_code.encode('ascii'))
        self._write_cfg(cfg, slot)
        # end of _write_scancode()

    def reset_slot(self, slot, current_access_code):
        """
        reset the given :slot:
        """
        self._write_scancode(
            self.yk_scan_code,
            slot,
            'h:000000000000',
            current_access_code,
        )
        time.sleep(1)
        cfg = self._ykdev.init_config(zap=True)
        self._write_cfg(cfg, slot)
        # end of reset_slot()

    def clear(self, current_access_code):
        """
        clear/reset all slots in the device
        """
        for slot in self.enabled_slots:
            self.reset_slot(slot, current_access_code)
        # end of clear()

    def initialize(self, oath_secret, otp_len, oath_tokenid, access_code):
        """
        do the complete initialization of both slots
        """
        self.init_hotp(1, oath_secret, otp_len, oath_tokenid, access_code)
        # NFC tied to disabled 2nd slot
        if self._ykdev.model == 'YubiKey NEO':
            self._ykdev.write_ndef(
                YubiKeyNEO_NDEF(
                    data=b'',
                    access_code=access_code.encode('ascii'),
                ),
                2,
            )
        # end of initialize()
