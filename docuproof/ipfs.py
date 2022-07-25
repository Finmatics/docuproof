from typing import Any

import ipfshttpclient as ipfs

from docuproof.encoders import uuid_aware_json_encode
from docuproof.meta import SingletonMeta


class IPFSClient(metaclass=SingletonMeta):
    def __new__(cls) -> "IPFSClient":
        cls.client = ipfs.connect(session=True)
        return super().__new__(cls)

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

    def get_json(self, hsh: str) -> dict[str, Any]:
        """
        Downloads a JSON object from IPFS and returns it.

        Args:
            hsh (str): IPFS hash.

        Returns:
            dict[str, Any]: JSON data.
        """
        return self.client.get_json(hsh)
