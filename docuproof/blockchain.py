import json
from functools import cached_property

import aiohttp
from eth_account.datastructures import SignedTransaction
from web3 import Web3
from web3.middleware import geth_poa_middleware

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
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            async with session.get(url) as response:
                return await response.text(encoding="utf-8")

    async def connect(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(Config.BLOCKCHAIN_PROVIDER_URL))
        if Config.POA_BLOCKCHAIN:
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.web3.isConnected():
            raise Exception("Could not connect to Ethereum node")

        abi = await self.abi
        self.contract = self.web3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=abi)

    def _get_nonce(self) -> int:
        """
        Returns the nonce of the configured wallet.
        """
        return self.web3.eth.get_transaction_count(Config.FROM_WALLET_ADDRESS)

    def _sign_transaction(self, txn: dict) -> SignedTransaction:
        """
        Signs a transaction with the configured private key.

        Args:
            txn (dict): Transaction to sign.

        Returns:
            dict: Signed transaction.
        """
        return self.web3.eth.account.sign_transaction(txn, private_key=Config.FROM_WALLET_PRIVATE_KEY)

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
        func_txn = self.contract.functions.addFile(uuid, ipfs_hash).build_transaction(
            {
                "from": Config.FROM_WALLET_ADDRESS,
                "nonce": self._get_nonce(),
            }
        )
        signed_txn = self._sign_transaction(func_txn)
        return self.web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()

    def add_files(self, uuids: list[str], ipfs_hash: str) -> str:
        """
        Executes the contract's addFiles function.
        Gas is estimated and the transaction is sent.

        Args:
            uuids (list[str]): UUIDs of files
            ipfs_hash (str): IPFS hash of the batch

        Returns:
            str: Transaction hash
        """
        func_txn = self.contract.functions.addFiles(uuids, ipfs_hash).build_transaction(
            {
                "from": Config.FROM_WALLET_ADDRESS,
                "nonce": self._get_nonce(),
            }
        )
        signed_txn = self._sign_transaction(func_txn)
        return self.web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()

    def get_ipfs_hash(self, uuid: str) -> None:
        """
        Executes the contract's getIPFSHash function.
        This function is free.

        Args:
            uuid (str): UUID of the file.
        """
        return self.contract.functions.getIPFSHash(uuid).call()
