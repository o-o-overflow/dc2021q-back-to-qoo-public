"""
This is a private file
"""


class SecretPlayer(object):
    def __init__(self):
        pass

    def secret_protocol(self, _, hacker, plays):
        # prepare a decend amount of epr pairs for further use
        for i in range(plays):
            q_id, ack_arrived = self.host.send_epr(hacker.host.host_id, await_ack=True)
            if ack_arrived:
                self.qubits.append(self.host.get_epr(hacker.host.host_id, q_id=q_id))
                self.q_ids.append(q_id)
