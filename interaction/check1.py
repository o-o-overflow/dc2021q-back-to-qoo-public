#!/usr/bin/env python3

from nclib import netcat
import sys


def main():

    host = sys.argv[1]
    port = int(sys.argv[2])

    conn = netcat.Netcat((host, port))

    conn.sendline(b'3')

    result = conn.recvuntil(b'Selection does not exist. Lose!\n', timeout=10)

    assert result is not None


if __name__ == '__main__':
    main()
