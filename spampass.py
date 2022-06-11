#!/usr/bin/env python
# Reference: https://pypi.org/project/dkimpy/

from __future__ import print_function

import sys
import argparse
import re
import datetime
from email import utils

import dkim


def main():
    # Backward compatibility hack because argparse doesn't support optional
    # positional arguments
    arguments=['--'+arg if arg[:8] == 'identity' else arg for arg in sys.argv[1:]]
    parser = argparse.ArgumentParser(
        description='Produce DKIM signature for email messages.',
        epilog="message to be signed follows commands on stdin")
    parser.add_argument('selector', action="store")
    parser.add_argument('domain', action="store")
    parser.add_argument('privatekeyfile', action="store")
    parser.add_argument('--hcanon', choices=['simple', 'relaxed'],
        default='relaxed',
        help='Header canonicalization algorithm: default=relaxed')
    parser.add_argument('--bcanon', choices=['simple', 'relaxed'],
        default='simple',
        help='Body canonicalization algorithm: default=simple')
    parser.add_argument('--signalg', choices=['rsa-sha256', 'ed25519-sha256', 'rsa-sha1'],
        default='rsa-sha256',
        help='Signature algorithm: default=rsa-sha256')
    parser.add_argument('--identity', help='Optional value for i= tag.')
    args=parser.parse_args(arguments)
    include_headers = None
    length = None
    logger = None

    if sys.version_info[0] >= 3:
        args.selector = bytes(args.selector, encoding='UTF-8')
        args.domain = bytes(args.domain, encoding='UTF-8')
        if args.identity is not None:
            args.identity = bytes(args.identity, encoding='UTF-8')
        args.hcanon = bytes(args.hcanon, encoding='UTF-8')
        args.bcanon = bytes(args.bcanon, encoding='UTF-8')
        args.signalg = bytes(args.signalg, encoding='UTF-8')
        # Make sys.stdin and stdout binary streams.
        sys.stdin = sys.stdin.detach()
        sys.stdout = sys.stdout.detach()
    canonicalize = (args.hcanon, args.bcanon)

    envelope = sys.stdin.read().decode()
    header = re.split("data\n", envelope, flags=re.IGNORECASE)[0] + "DATA\n"
    message = re.split("data\n", envelope, flags=re.IGNORECASE)[1].split("\n.\n")[0]
    delimiter = "\n.\n" # End Data <CR><LF>.<CR><LF>

    # add date header
    if not re.search('^DATE: ', message, re.IGNORECASE):
        n = datetime.datetime.now(datetime.timezone.utc)
        message = "DATE: %s\n" % utils.format_datetime(n) + message

    # Message-Id header
    if not re.search('^Message-Id: ', message, re.IGNORECASE):
        message = "Message-Id: %s\n" % utils.make_msgid(domain=args.domain.decode()) + message

    d = dkim.DKIM(message.encode(),logger=logger, signature_algorithm=args.signalg,
                  linesep=dkim.util.get_linesep(message.encode()))
    sig = d.sign(args.selector, args.domain, open(
                 args.privatekeyfile, "rb").read(), identity = args.identity,
                 canonicalize=canonicalize, include_headers=include_headers,
                 length=length)

    sys.stdout.write(header.encode())
    sys.stdout.write(sig)
    sys.stdout.write(message.encode())
    sys.stdout.write(delimiter.encode()) 

if __name__ == "__main__":
    main()
