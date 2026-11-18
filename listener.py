
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
from pathlib import Path
import json
from datetime import datetime
import pandas as pd


def scan_blocks(chain, start_block, end_block,
                contract_address,
                eventfile='deposit_logs.csv'):

    # Connect to the blockchain
    if chain == 'avax':
        api_url = "https://api.avax-test.network/ext/bc/C/rpc"

    elif chain == 'bsc':
        api_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"

    else:
        raise ValueError("Invalid chain")

    w3 = Web3(Web3.HTTPProvider(api_url))

    w3.middleware_onion.inject(
        ExtraDataToPOAMiddleware, layer=0
    )

    # Deposit event ABI
    DEPOSIT_ABI = json.loads('''
    [
        {
            "anonymous": false,
            "inputs": [
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "token",
                    "type": "address"
                },
                {
                    "indexed": true,
                    "internalType": "address",
                    "name": "recipient",
                    "type": "address"
                },
                {
                    "indexed": false,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "Deposit",
            "type": "event"
        }
    ]
    ''')

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=DEPOSIT_ABI
    )

    # Resolve latest block
    if start_block == "latest":
        start_block = w3.eth.get_block_number()

    if end_block == "latest":
        end_block = w3.eth.get_block_number()

    # Validate block range
    if end_block < start_block:
        print("Error end_block < start_block!")
        return

    if start_block == end_block:
        print(f"Scanning block {start_block} on {chain}")
    else:
        print(
            f"Scanning blocks {start_block} - "
            f"{end_block} on {chain}"
        )

    # Store deposit events
    deposit_data = []

    # Scan blocks in batches of 30
    # Use get_logs instead of create_filter
    for first_block in range(start_block, end_block + 1, 30):

        last_block = min(first_block + 29, end_block)

        events = contract.events.Deposit.get_logs(
            from_block=first_block,
            to_block=last_block,
            argument_filters={}
        )

        # Process Deposit events
        for evt in events:

            data = {
                'chain': chain,
                'token': evt.args['token'],
                'recipient': evt.args['recipient'],
                'amount': evt.args['amount'],
                'transactionHash': Web3.to_hex(
                    evt.transactionHash
                ),
                'address': evt.address,
                'date': datetime.now().strftime(
                    "%m/%d/%Y %H:%M:%S"
                )
            }

            deposit_data.append(data)

    # Required CSV columns
    columns = [
        'chain',
        'token',
        'recipient',
        'amount',
        'transactionHash',
        'address',
        'date'
    ]

    # Create DataFrame
    df = pd.DataFrame(
        deposit_data,
        columns=columns
    )

    # Determine whether to write CSV header
    file_path = Path(eventfile)

    write_header = (
        not file_path.exists()
        or file_path.stat().st_size == 0
    )

    # Append events to CSV
    df.to_csv(
        eventfile,
        mode='a',
        header=write_header,
        index=False
    )

    print(f"Recorded {len(deposit_data)} Deposit events")
