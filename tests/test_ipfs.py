from docuproof.ipfs import IPFSClient


def test_ipfs_client_same_instance() -> None:
    client1 = IPFSClient()
    client2 = IPFSClient()
    assert client1 == client2


def test_ipfs_client_upload_json() -> None:
    client = IPFSClient()
    client.connect()
    tx_hash = client.upload_json({"test": "test"})

    assert type(tx_hash) is str
    assert tx_hash != ""


def test_ipfs_client_get_json() -> None:
    client = IPFSClient()
    client.connect()
    tx_hash = client.upload_json({"test": "test"})

    data = client.get_json(tx_hash)

    assert data == {"test": "test"}
