from brownie import DocuProof, accounts


def main() -> None:
    acc = accounts[0]
    DocuProof.deploy({"from": acc})
