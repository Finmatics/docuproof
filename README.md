# DocuProof

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

## Testing

To run the complete test suite:
```
$ brownie test
```
