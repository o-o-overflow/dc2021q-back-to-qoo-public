"""
This is private file
"""
from players import zardus, hacker, ZARDUS_ID


def secret(id):
    return hacker.host.get_epr(ZARDUS_ID, zardus.q_ids[id])
