import json
from functools import cached_property

import aiohttp
from web3 import Web3

from docuproof.config import Config
from docuproof.meta import SingletonMeta


class DocuProofContract(metaclass=SingletonMeta):
    @cached_property
    async def abi(self) -> str:
        path = Config.BASE_DIR / "build" / "contracts" / "DocuProof.json"
        if path.exists():
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
                return json.dumps(data["abi"])

        url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={Config.CONTRACT_ADDRESS}&format=raw"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text(encoding="utf-8")

    async def connect(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(Config.BLOCKCHAIN_PROVIDER_URL))

        if not self.web3.isConnected():
            raise Exception("Could not connect to Ethereum node")

        abi = await self.abi
        self.contract = self.web3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=abi)

    def add_file(self, uuid: str, ipfs_hash: str) -> str:
        """
        Executes the contract's addFile function.
        Gas is estimated and the transaction is sent.

        Args:
            uuid (str): UUID of a file
            ipfs_hash (str): IPFS hash of the batch

        Returns:
            str: Transaction hash
        """
        return self.contract.functions.addFile(uuid, ipfs_hash).transact({"from": Config.FROM_WALLET_ADDRESS})

    def add_files(self, uuids: list[str], ipfs_hash: str) -> None:
        """
        Executes the contract's addFiles function.
        Gas is estimated and the transaction is sent.

        Args:
            uuids (list[str]): UUIDs of files
            ipfs_hash (str): IPFS hash of the batch

        Returns:
            str: Transaction hash
        """
        return self.contract.functions.addFiles(uuids, ipfs_hash).transact({"from": Config.FROM_WALLET_ADDRESS})

    def get_ipfs_hash(self, uuid: str) -> None:
        """
        Executes the contract's getIPFSHash function.
        This function is free.

        Args:
            uuid (str): UUID of the file.
        """
        return self.contract.functions.getIPFSHash(uuid).call()
