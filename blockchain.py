# ============================================================
# blockchain.py  — PERSON 1's file
# Handles the core blockchain: blocks, hashing, chain validity
# NOW WITH: save/load support so data survives server restarts
# ============================================================

import hashlib
import json
import time


class Block:
    """A single block in the chain. Stores a list of transactions."""

    def __init__(self, index, transactions, previous_hash,
                 timestamp=None, nonce=0, hash=None):
        self.index = index
        # Use provided timestamp (when loading) or generate new one
        self.timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        # Use provided hash (when loading) or calculate fresh
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        """SHA-256 hash of the block contents."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        """
        Proof-of-Work: keep changing nonce until hash starts with
        difficulty number of zeros. Makes the chain tamper-proof.
        """
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    @classmethod
    def from_dict(cls, data: dict):
        """
        Reconstruct a Block from a saved dictionary (from data.json).
        Skips mining — uses the saved hash directly.
        """
        return cls(
            index=data["index"],
            transactions=data["transactions"],
            previous_hash=data["previous_hash"],
            timestamp=data["timestamp"],
            nonce=data["nonce"],
            hash=data["hash"],
        )


class Blockchain:
    """The full chain. New blocks are added whenever a donation is recorded."""

    def __init__(self):
        self.chain = [self._create_genesis_block()]
        self.difficulty = 2

    # ── Genesis (first) block ──────────────────────────────────
    def _create_genesis_block(self):
        genesis = Block(0, [{"type": "GENESIS", "message": "Charity Chain Started"}], "0")
        return genesis

    # ── Load chain from saved list of dicts ───────────────────
    def load_from_list(self, chain_data: list):
        """
        Replaces the current chain with blocks rebuilt from saved data.
        Called on startup when data.json exists.
        """
        self.chain = [Block.from_dict(b) for b in chain_data]

    # ── Add a transaction (donation event) ────────────────────
    def add_transaction(self, transaction: dict) -> str:
        """
        Mines a new block containing transaction and appends it.
        Returns the new block's hash (the donor's tracking ID).
        """
        new_block = Block(
            index=len(self.chain),
            transactions=[transaction],
            previous_hash=self.get_latest_block().hash,
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block.hash

    # ── Helpers ───────────────────────────────────────────────
    def get_latest_block(self):
        return self.chain[-1]

    def is_chain_valid(self) -> bool:
        """
        Recalculates every block's hash and checks links.
        Returns False if anything has been tampered with.
        """
        for i in range(1, len(self.chain)):
            current  = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def get_all_transactions(self) -> list:
        """Return every transaction across all blocks (skips genesis)."""
        txs = []
        for block in self.chain[1:]:
            for tx in block.transactions:
                txs.append({
                    **tx,
                    "block_index": block.index,
                    "block_hash":  block.hash,
                    "timestamp":   block.timestamp,
                })
        return txs

    def find_transaction(self, tx_hash: str):
        """Look up a specific transaction by block hash (the tracking ID)."""
        for block in self.chain[1:]:
            if block.hash == tx_hash:
                tx = block.transactions[0] if block.transactions else {}
                return {
                    **tx,
                    "block_index": block.index,
                    "block_hash":  block.hash,
                    "timestamp":   block.timestamp,
                }
        return None

    def to_dict(self) -> list:
        """Serialise the entire chain — used for display and for saving."""
        result = []
        for block in self.chain:
            result.append({
                "index":         block.index,
                "timestamp":     block.timestamp,
                "transactions":  block.transactions,
                "previous_hash": block.previous_hash,
                "hash":          block.hash,
                "nonce":         block.nonce,
            })
        return result
