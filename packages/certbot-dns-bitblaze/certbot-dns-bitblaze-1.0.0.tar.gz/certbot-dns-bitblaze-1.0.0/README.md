certbot-dns-bitblaze
============

![Tests](https://github.com/lehuizi/certbot-dns-bitblaze/workflows/Tests/badge.svg)
![Upload Python Package](https://github.com/lehuizi/certbot-dns-bitblaze/workflows/Upload%20Python%20Package/badge.svg)
[![Python Version](https://img.shields.io/pypi/pyversions/certbot-dns-bitblaze)](https://pypi.org/project/certbot-dns-bitblaze/)
[![PyPi Status](https://img.shields.io/pypi/status/certbot-dns-bitblaze)](https://pypi.org/project/certbot-dns-bitblaze/)
[![Version](https://img.shields.io/github/v/release/lehuizi/certbot-dns-bitblaze)](https://pypi.org/project/certbot-dns-bitblaze/)

bitblaze DNS Authenticator plugin for [Certbot](https://certbot.eff.org/).

This plugin is built from the ground up and follows the development style and life-cycle
of other `certbot-dns-*` plugins found in the
[Official Certbot Repository](https://github.com/certbot/certbot).

Installation
------------

```
pip install --upgrade certbot # optional
pip install certbot-dns-bitblaze
```

Verify:

```
$ certbot plugins --text

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
* dns-bitblaze
Description: Obtain certificates using a DNS TXT record by using the bitblaze
dns api.
Interfaces: IAuthenticator, IPlugin
Entry point: dns-bitblaze = certbot_dns_bitblaze.dns_bitblaze:Authenticator

...
...
```

Configuration
-------------

The credentials file e.g. `~/bbdns-credentials.ini` should look like this:

```
dns_bitblaze_token=put_your_token_here
```

Usage
-----


```
certbot certonly --authenticator dns-bitblaze --dns-bitblaze-credentials=~/bbdns-credentials.ini -d bitblaze.io
```
