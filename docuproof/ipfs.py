from typing import Any

import ipfshttpclient as ipfs

from docuproof.encoders import uuid_aware_json_encode


class IPFSClient:
    def __init__(self) -> None:
        self.client = ipfs.connect(session=True)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self.client.close()

    def upload_json(self, data: dict[str, Any]) -> str:
        """
        Uploads a JSON object to IPFS and returns the hash.

        Args:
            data (dict[str, Any]): JSON data to upload.

        Returns:
            str: IPFS hash.
        """
        return self.client.add_bytes(uuid_aware_json_encode(data))
