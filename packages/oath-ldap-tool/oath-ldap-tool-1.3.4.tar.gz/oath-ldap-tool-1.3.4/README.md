OATH-LDAP services
==================

[OATH-LDAP](https://oath-ldap.stroeder.com/) directly integrates
OTP-based two-factor authentication into
[OpenLDAP](https://www.openldap.org) *slapd*.

This is the command-line tool for various use-cases:
  * Generate asymmetric primary key pairs used for encrypting
    the OATH shared secrets
  * Add LDAP entries for hardware OTP devices
  * Initialize a Yubikey slot over USB

Requirements
------------

  * Python 3.6+
