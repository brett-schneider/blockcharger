pragma solidity ^0.6.1;


contract Registration {

    struct Provider{
        uint id;
        address provider_address;
        string location;
    }

    mapping(uint => Provider) public energy_providers;
    uint numProviders;
    // Provider[] public energy_providers;


    constructor() internal {
        numProviders = 0;
    }


    function getAllProviders() public view returns (address[] memory){
        address[] memory all = new address[](numProviders);
        // Provider[] memory all = new Provider[](numProviders);
        for (uint i = 0; i < numProviders; i++) {
            all[i] = energy_providers[i].provider_address;
        }
        return all;
    }


    function getProviderLocation(uint providerID) public view returns (string memory location) {
       return energy_providers[providerID].location;
    }


    function registerProvider(address _address, string memory _location) public returns (uint providerID) {
        providerID = numProviders;
        energy_providers[providerID] = Provider(providerID, _address, _location);
        numProviders++;
        return providerID;
    }

}
    
