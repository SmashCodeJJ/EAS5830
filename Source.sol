// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract Source is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant WARDEN_ROLE = keccak256("BRIDGE_WARDEN_ROLE");
	mapping( address => bool) public approved;
	address[] public tokens;

	event Deposit( address indexed token, address indexed recipient, uint256 amount );
	event Withdrawal( address indexed token, address indexed recipient, uint256 amount );
	event Registration( address indexed token );

    constructor( address admin ) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(ADMIN_ROLE, admin);
        _grantRole(WARDEN_ROLE, admin);

    }

	function deposit(address _token, address _recipient, uint256 _amount ) public {
		//YOUR CODE HERE
    // Check that the token is registered
    require(
        approved[_token],
        "Token not registered"
    );

    // Transfer tokens from user to bridge contract
    bool success = ERC20(_token).transferFrom(
        msg.sender,
        address(this),
        _amount
    );

    require(success, "Token transfer failed");

    // Emit deposit event
    emit Deposit(
        _token,
        _recipient,
        _amount
    );
	}

	function withdraw(address _token, address _recipient, uint256 _amount ) onlyRole(WARDEN_ROLE) public {
		//YOUR CODE HERE
    // Transfer tokens to recipient
    bool success = ERC20(_token).transfer(
        _recipient,
        _amount
    );

    require(success, "Token withdrawal failed");

    // Emit withdrawal event
    emit Withdrawal(
        _token,
        _recipient,
        _amount
    );
	}

	function registerToken(address _token) onlyRole(ADMIN_ROLE) public {
		//YOUR CODE HERE
    // Ensure token has not already been registered
    require(
        !approved[_token],
        "Token already registered"
    );

    // Reject zero address
    require(
        _token != address(0),
        "Invalid token address"
    );

    // Mark the token as approved
    approved[_token] = true;

    // Add token to registered token list
    tokens.push(_token);

    // Emit registration event
    emit Registration(_token);
}
	}





