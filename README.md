# DocuProof

## Installation

* Install Brownie
```
$ python3 -m pip install --user pipx
$ pipx install eth-brownie
```

* Install dependencies
```
$ python3 -m pip install -r requirements.txt
```

* Connect with IPFS and Ethereum node

  1. (Recommended) Use [Infura](https://infura.io/) to obtain credentials for the IPFS and Ethereum endpoints and add them to `.env` file using the template
  2. Run both nodes locally - you can do so with Docker:
   ```
   $ docker run -d -p 7545:8545 trufflesuite/ganache-cli:latest
   $ docker run -d -p 4001:4001 -p 8080:8080 -p 5001:5001 ipfs/go-ipfs:latest
   ```

## Usage

### Compiling contracts

To compile all of the contract sources within the `contracts/` subfolder of the project:
```
$ brownie compile
```

You can also interact with the contracts using the brownie console:
```
$ brownie console
```

### Using Ganache GUI with Brownie

In order to use the local blockchain managed by Ganache, we need to add its network to Brownie:
```
$ brownie networks add Live ganache-gui host=http://127.0.0.1:7545 chainid=5777 name="Ganache GUI"
```

### Running the application

In order to run the application using the built-in Sanic server:

```
$ python3 -m sanic docuproof.app:application
```

## Deployment

To deploy the smart contract to Ethereum MainNet, we can use the following Brownie command:
```
$ export FROM_WALLET_PRIVATE_KEY=<YOUR-WALLET-PRIVATE-KEY>
$ brownie run scripts/deploy.py --network mainnet
```

### Additional test networks

In order to deploy the smart contract to a test network which wasn't included by default, we can use the following Brownie command:
```
# Sepolia
$ brownie networks add Ethereum sepolia \
  host='https://sepolia.infura.io/v3/$WEB3_INFURA_PROJECT_ID' \
  chainid=11155111 \
  name='Sepolia (Infura)' \
  explorer='https://api-sepolia.etherscan.io/api' \
  multicall2='0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696' \
  provider=infura
```

## Testing

To run the complete test suite:
```
$ pytest
```
