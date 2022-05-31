pragma solidity ^0.5.0;

import "./KrishTokenMintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

contract KrishTokenCrowdsale is Crowdsale, MintedCrowdsale {
    constructor(
        uint256 rate, // rate in TKNbits - uint256 and uint are interchangeable - https://docs.soliditylang.org/en/v0.4.21/types.html#value-types
        address payable wallet, // sale beneficiary
        KrishToken token // the KrishToken itself that the KrishTokenCrowdsale will work with
    )
      Crowdsale(rate, wallet, token)
      public
    {
        // constructor can stay empty
    }
}

contract KrishTokenCrowdsaleDeployer {
    address public Krish_token_address;
    address public Krish_crowdsale_address;

    constructor(
        string memory name,
        string memory symbol,
        address payable wallet // this address will receive all Ether raised by the sale
    ) public {
        // create the KrishToken and keep its address handy
        KrishToken token = new KrishToken(name, symbol, 0);
        Krish_token_address = address(token);

        // create the KrishTokenCrowdsale and tell it about the token
        KrishTokenCrowdsale Krish_crowdsale =
            new KrishTokenCrowdsale(1, wallet, token);
        Krish_crowdsale_address = address(Krish_crowdsale);

        // make the KrishTokenCrowdsale contract a minter,
        // then have the KrishTokenCrowdsaleDeployer renounce its minter role
        token.addMinter(Krish_crowdsale_address);
        token.renounceMinter();
    }
}
