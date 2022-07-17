// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract DocuProof is Ownable {
    mapping(string => IPFSObject) collection;

    struct IPFSObject {
        string ipfsHash;
        bool exists;
    }

    event FileAdded(string indexed uuid, string indexed ipfsHash);

    function addFile(string calldata _uuid, string calldata _ipfsHash)
        public
        onlyOwner
    {
        require(
            collection[_uuid].exists == false,
            "This UUID already exists in contract."
        );

        IPFSObject memory obj = IPFSObject(_ipfsHash, true);
        collection[_uuid] = obj;

        emit FileAdded(_uuid, _ipfsHash);
    }

    function addFiles(string[] calldata _uuids, string calldata _ipfsHash)
        public
        onlyOwner
    {
        for (uint256 i = 0; i < _uuids.length; i++) {
            addFile(_uuids[i], _ipfsHash);
        }
    }

    function getIPFSHash(string calldata _uuid)
        public
        view
        returns (string memory)
    {
        require(
            collection[_uuid].exists == true,
            "This UUID does not exist in contract."
        );

        return collection[_uuid].ipfsHash;
    }
}
