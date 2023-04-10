import pytest

from docuproof.config import Config
from docuproof.ipfs import IPFSClient
from docuproof.utils import convert_url_to_multiaddr


@pytest.fixture
def ipfs_client() -> IPFSClient:
    ipfs_addr = convert_url_to_multiaddr(Config.IPFS_API_ENDPOINT) if Config.IPFS_API_ENDPOINT else None
    ipfs_auth = (
        (Config.IPFS_ENDPOINT_USERNAME, Config.IPFS_ENDPOINT_PASSWORD)
        if Config.IPFS_ENDPOINT_USERNAME and Config.IPFS_ENDPOINT_PASSWORD
        else None
    )
    ipfs_client = IPFSClient()
    ipfs_client.connect(
        addr=ipfs_addr,
        auth=ipfs_auth,
    )
    return ipfs_client


def test_ipfs_client_same_instance() -> None:
    client1 = IPFSClient()
    client2 = IPFSClient()
    assert client1 == client2


def test_ipfs_client_upload_json(ipfs_client: IPFSClient) -> None:
    tx_hash = ipfs_client.upload_json({"test": "test"})

    assert type(tx_hash) is str
    assert tx_hash != ""


def test_ipfs_client_get_json(ipfs_client: IPFSClient) -> None:
    tx_hash = ipfs_client.upload_json({"test": "test"})

    data = ipfs_client.get_json(tx_hash)

    assert data == {"test": "test"}
