from brownie import DocuProof, accounts, config


def main() -> None:
    acc = accounts.add(config["wallets"]["from_key"])
    contract = DocuProof.deploy({"from": acc})
    print(f"Contract deployed to {contract.address}")
