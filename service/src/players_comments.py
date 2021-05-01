"""
This is a public file
"""
from qunetsim.components import Host
import logging
import random
import hashlib
from Crypto.Cipher import AES
from secret_player import SecretPlayer

logger = logging.getLogger("players")
logger.setLevel("WARNING")

ZARDUS_ID = "zardus"
HACKER_ID = "Hacker"
ADAMD_ID = "adamd"

FLAG = b"flagflag"

# TODO: clean it up, remove comments and debug information


class Player(object):
    def __init__(self):
        pass

    def get_next_classical_message(self, receiver_id, buffer, count):
        buffer = buffer + self.host.get_classical(receiver_id, wait=-1)
        msg = "ACK"
        while msg == "ACK" or (msg.split(':')[0] != ("%d" % count)):
            if len(buffer) == 0:
                buffer = buffer + self.host.get_classical(receiver_id, wait=-1)
            ele = buffer.pop(0)
            msg = ele.content
        return msg

    def key_array_to_key_string(self, key_list):
        key_string_binary = b''.join([bytes([x]) for x in key_list])
        return hashlib.md5(key_string_binary).digest()


class Zardus(Player, SecretPlayer):
    def __init__(self):
        self.host = Host(ZARDUS_ID)
        self.host.add_connection(HACKER_ID)
        self.host.add_connection(ADAMD_ID)
        self.host.delay = 0
        self.host.start()
        self.qubits = []
        self.q_ids = []
        self.bases = []

    def bet(self, gameid, referee):
        qubit = self.qubits[gameid]
        # if referee is 0, then use |0>, |1> basis
        # else use |+> and |-> basis
        if referee == 1:
            qubit.H()
            res = qubit.measure(non_destructive=True)
            qubit.H()
        else:
            res = qubit.measure(non_destructive=True)
        self.bases.append(referee)
        return res

    def chat(self, host, adamd_id, qubits_n):
        q_i = 0
        msg_buff = []
        secret_key = []

        for q_i, qubit in enumerate(self.qubits):
            self.host.send_qubit(adamd_id, qubit, await_ack=True)

            message = self.get_next_classical_message(adamd_id, msg_buff, q_i)
            print(f"{host.host_id} receives from {adamd_id}: {message}")

            if message == f"{q_i}:{self.bases[q_i]}":
                logger.info(f"{host.host_id}: qubit {q_i} is correct")
                if self.bases[q_i] == 1:
                    qubit.H()
                    res = qubit.measure(non_destructive=True)
                    qubit.H()
                else:
                    res = qubit.measure(non_destructive=True)

                secret_key.append(res)
                msg = f"{q_i}:0"
            else:
                msg = f"{q_i}:1"

            self.host.send_classical(adamd_id, msg, await_ack=True)

        nonce_msg = self.get_next_classical_message(adamd_id, msg_buff, -1)
        ciphertext_msg = self.get_next_classical_message(adamd_id, msg_buff, -2)
        print(f"{host.host_id} receives from {adamd_id}: {nonce_msg}")
        print(f"{host.host_id} receives from {adamd_id}: {ciphertext_msg}")


class Adamd(Player):
    def __init__(self):
        self.host = Host(ADAMD_ID)
        self.host.add_connection(ZARDUS_ID)
        self.host.delay = 0
        self.host.start()
        self.wait_time = 1

    def chat(self, host, zardus_id, qubits_n):
        logger.debug(f"Adamd's chat Start")

        msg_buff = []
        q_i = 0
        secret_key = []

        while q_i < qubits_n:
            # 1. receive the qubit from Zardus / Yan
            logger.debug(f"Adamd: Getting qubit from Zardus")
            qubit = self.host.get_data_qubit(zardus_id, wait=self.wait_time)
            while qubit is None:
                qubit = self.host.get_data_qubit(zardus_id, wait=self.wait_time)

            # 2. randomly generate a measurement basis
            logger.debug(f"Adamd: generating a measurement basis")
            basis = random.randint(0, 1)

            # 3. send the measurement basis to zardus
            logger.debug(f"Adamd: sending message {q_i}:{basis}")
            self.host.send_classical(zardus_id, f"{q_i}:{basis}", await_ack=True)

            # 4. get the measurement message from zardus
            msg = self.get_next_classical_message(zardus_id, msg_buff, q_i)
            logger.debug(f"Adamd: Getting message from Zardus {msg}")

            if msg == f"{q_i}:0":
                logger.debug(f"Adamd: qubit {q_i} is correct!")
                if basis == 1:
                    qubit.H()
                logger.debug(f"Adamd: start measuring")
                bit = qubit.measure(non_destructive=True)
                logger.debug(f"Adamd: finish measuring")
                secret_key.append(bit)
            q_i += 1

        logger.info(f"Adamd's secret key: {secret_key}")
        key = self.key_array_to_key_string(secret_key)
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        with open('/flag', 'rb') as f:
            data = f.read()
        ciphertext = cipher.encrypt(data)
        self.host.send_classical(zardus_id, f"-1:{nonce.hex()}", await_ack=True)
        self.host.send_classical(zardus_id, f"-2:{ciphertext.hex()}", await_ack=True)


class Hacker(Player):
    def __init__(self):
        self.host = Host(HACKER_ID)
        self.host.add_connection(ZARDUS_ID)
        self.host.deley = 0
        self.host.start()


adamd = Adamd()
zardus = Zardus()
hacker = Hacker()
