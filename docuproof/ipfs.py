from typing import Any, Optional

import ipfshttpclient as ipfs

from docuproof.encoders import uuid_aware_json_encode
from docuproof.meta import SingletonMeta


class IPFSClient(metaclass=SingletonMeta):
    def connect(self, addr: Optional[str] = None, auth: Optional[tuple[str, str]] = None) -> None:
        connection_kwargs: dict[str, Any] = {}
        if addr:
            connection_kwargs["addr"] = addr
        if auth:
            connection_kwargs["auth"] = auth

        self.client = ipfs.connect(session=True, **connection_kwargs)

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
