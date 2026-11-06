#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, transactions):
    """
        k - Number of trailing zeros in the binary representation (integer)
        prev_hash - the hash of the previous block (bytes)
        rand_lines - a set of "transactions," i.e., data to be included in this block (list of strings)

        Complete this function to find a nonce such that 
        sha256( prev_hash + rand_lines + nonce )
        has k trailing zeros in its *binary* representation
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'

    # TODO your code to find a nonce here

    # Prepare the previous block hash and transactions
    block = hashlib.sha256()
    block.update(prev_hash)

    for transaction in transactions:
        block.update(transaction.encode("utf-8"))

    # Mask for checking the last k bits
    mask = (1 << k) - 1

    # Brute-force search
    n = 0

    while True:
        nonce = str(n).encode("utf-8")

        # Hash prev_hash + transactions + nonce
        candidate = block.copy()
        candidate.update(nonce)

        hash_value = candidate.digest()

        # Check whether last k bits are zero
        if int.from_bytes(hash_value, "big") & mask == 0:
            break

        n += 1

    assert isinstance(nonce, bytes), 'nonce should be of type bytes'
    return nonce


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 15

    # Generate a previous block hash
    prev_hash = os.urandom(32)

    # Get random transactions
    transactions = get_random_lines(filename, num_lines)

    # Mine the block
    nonce = mine_block(diff, prev_hash, transactions)

    print("Nonce found:", nonce)

    # Verify the block hash
    block_data = prev_hash

    for transaction in transactions:
        block_data += transaction.encode("utf-8")

    block_hash = hashlib.sha256(
        block_data + nonce
    ).digest()

    print("Block hash:", block_hash.hex())

    # Check proof of work
    valid = int.from_bytes(block_hash, "big") % (2 ** diff) == 0

    print("Valid Proof of Work:", valid)
