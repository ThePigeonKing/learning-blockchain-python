import hashlib
import json
from textwrap import dedent
from threading import RLock
from time import time
from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        # lock for async endpoints in fastapi
        self._lock = RLock()
        # generating id on init instead of flas app
        self.node_id: str = str(uuid4()).replace("-", "")
        # list of blocks
        self.chain: list = []
        # list of transactions to be added in new block
        self.current_transactions: list = []

        # create genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof: int, previous_hash: str | None) -> dict:
        with self._lock:
            # create a new Block and add it to the chain
            block = {
                "index": len(self.chain) + 1,
                "timestamp": time(),
                "transactions": self.current_transactions,
                "proof": proof,
                "previous_hash": previous_hash or self.hash(self.chain[-1]),
            }

            # reset current transactions
            self.current_transactions = []

            self.chain.append(block)
            return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        with self._lock:
            # create a new transaction to the existing list
            new_transact = {"sender": sender, "recipient": recipient, "amount": amount}
            self.current_transactions.append(new_transact)

            if len(self.last_block) > 0:
                return self.last_block["index"] + 1
            else:
                raise IndexError(
                    f"self.last_block = {self.last_block}, impossible to find last index"
                )

    @staticmethod
    def hash(block: dict):
        # get hash of block
        block_str = json.dumps(block, sort_keys=True).encode()
        newhash = hashlib.sha256(block_str).hexdigest()

        return newhash

    @property
    def last_block(self) -> dict:
        with self._lock:
            # return the last block in chain
            if len(self.chain) == 0:
                raise ValueError("Chain list is empty, can't find last element")

            return self.chain[-1]

    # Proof of Work implementation
    def proof_of_work(self, last_proof: int):
        # find a number p1 such that hash(pp1) contain 4 leading '0' where p is the previous p1
        current_proof = 0
        while self.valid_proof(last_proof, current_proof) is False:
            current_proof += 1

        return current_proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int):
        # validate the proof for containing 4 leading '0', return True/False
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def __str__(self) -> str:
        with self._lock:
            line = f"""====== BLOCKCHAIN ======
    ID: {self.node_id}
    Current chain length: {len(self.chain)}
    Last chain element: {self.chain[-1]['index'] if len(self.chain) > 0 else None}
    Current transactions amount: {len(self.current_transactions)}
    Last transaction: {self.current_transactions[-1]['sender'] + '->' + self.current_transactions[-1]["recipient"] + " | " + str(self.current_transactions[-1]['amount']) if len(self.current_transactions) > 0 else None}
====== END ======"""
            line = dedent(line)
            return line

    def json_dict(self) -> dict:
        id = self.node_id
        chain_length = len(self.chain)
        last_chain_elem = self.chain[-1] if len(self.chain) > 0 else None
        current_transaction_amount = len(self.current_transactions)

        return {
            "id": id,
            "chain_length": chain_length,
            "last_chain_elem": last_chain_elem,
            "transaction_length": current_transaction_amount,
            "transactions": self.current_transactions,
        }
