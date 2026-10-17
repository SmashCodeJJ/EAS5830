import requests
import json

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJjYmI4ZmYzZi03ZjI1LTQ4MDktYWU3MC1kYmRjM2ZiNTJlZDMiLCJlbWFpbCI6InpodW9qZXJyeTFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiRlJBMSJ9LHsiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjEsImlkIjoiTllDMSJ9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjczOWRkNGVjNzcxM2VhNTk2YTFlIiwic2NvcGVkS2V5U2VjcmV0IjoiNzgyN2ViNjQwZDhiMWNlZWZlMmQxZDI0NzMwMTBmNTliMTRlZTQ1ZDVjNzNlZTE4YmVmZjYxYjE1NmIzOWM4NyIsImV4cCI6MTgyMzgwMDg1N30.WpqrtkZzKteFvfuxEC1qinQYfgmoNCLMe8Lxj7tn0CY"


def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    headers = {
        "Authorization": f"Bearer {PINATA_JWT}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    result = response.json()

    cid = result["IpfsHash"]

    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    url = f"https://gateway.pinata.cloud/ipfs/{cid}"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    assert isinstance(data, dict), "get_from_ipfs should return a dict"

    return data
  
if __name__ == "__main__":
    test_data = {
        "name": "test",
        "value": 123
    }

    cid = pin_to_ipfs(test_data)
    print("CID:", cid)

    data = get_from_ipfs(cid)
    print("Retrieved:", data)