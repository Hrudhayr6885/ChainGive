// ============================================================
// smart_contract.sol  — PERSON 1's file (converted from Python)
// Solidity Smart Contract:
//   - registers charities & beneficiaries
//   - validates donations
//   - controls fund release
//   - fraud checks
// ============================================================

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CharityBlockchain {

    // ── Owner / Admin ─────────────────────────────────────────
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only admin can call this function.");
        _;
    }

    // ── Data Structures ───────────────────────────────────────

    struct Charity {
        string  name;
        address wallet;
        bool    verified;
        uint256 balance;   // stored in wei
    }

    struct Beneficiary {
        string  name;
        string  charityId;
        bool    verified;
        uint256 fundsReceived;   // stored in wei
    }

    // ── Storage ───────────────────────────────────────────────

    mapping(string => Charity)     public charities;
    mapping(string => Beneficiary) public beneficiaries;

    string[] public charityIds;
    string[] public beneficiaryIds;

    uint256 public totalDonated;
    uint256 public totalReleased;
    uint256 public totalDonationCount;

    // ── Events (equivalent to blockchain.add_transaction) ─────

    event DonationReceived(
        string  indexed charityId,
        string  charityName,
        address indexed donor,
        string  donorName,
        uint256 amount,
        string  message,
        string  status
    );

    event FundsReleased(
        string  indexed charityId,
        string  charityName,
        string  indexed beneficiaryId,
        string  beneficiaryName,
        uint256 amount,
        string  status
    );

    event BeneficiaryVerified(
        string  indexed beneficiaryId,
        string  beneficiaryName,
        string  status
    );

    event BeneficiaryAdded(
        string  beneficiaryId,
        string  name,
        string  charityId
    );

    // ── Constructor ───────────────────────────────────────────

    constructor() {
        owner = msg.sender;

        // ── Default Charities (mirrors DEFAULT_CHARITIES in Python) ──
        _addCharity("C001", "Feed the Hungry",   0xFEED001000000000000000000000000000000000);
        _addCharity("C002", "Education for All", 0xEDUC002000000000000000000000000000000000);
        _addCharity("C003", "Health Aid Fund",   0xHEAL003000000000000000000000000000000000);

        // ── Default Beneficiaries (mirrors DEFAULT_BENEFICIARIES) ───
        _addDefaultBeneficiary("B001", "Ananya Sharma", "C001", true);
        _addDefaultBeneficiary("B002", "Ravi Kumar",    "C002", true);
        _addDefaultBeneficiary("B003", "Priya Nair",    "C003", false);
    }

    // ── Internal helpers for constructor ─────────────────────

    function _addCharity(
        string memory id,
        string memory name,
        address wallet
    ) internal {
        charities[id] = Charity({
            name:     name,
            wallet:   wallet,
            verified: true,
            balance:  0
        });
        charityIds.push(id);
    }

    function _addDefaultBeneficiary(
        string memory id,
        string memory name,
        string memory charityId,
        bool verified
    ) internal {
        beneficiaries[id] = Beneficiary({
            name:          name,
            charityId:     charityId,
            verified:      verified,
            fundsReceived: 0
        });
        beneficiaryIds.push(id);
    }

    // ─────────────────────────────────────────────────────────
    //  PUBLIC CONTRACT FUNCTIONS
    // ─────────────────────────────────────────────────────────

    /**
     * @notice Records a donation to a specific charity.
     * @dev    Equivalent to donate() in smart_contract.py.
     *         msg.value carries the ETH amount.
     *
     * Solidity equivalent of:
     *   function donate(string charityId) external payable { ... }
     */
    function donate(
        string calldata donorName,
        string calldata charityId,
        string calldata message
    ) external payable {

        // ── Validation ────────────────────────────────────────
        require(
            bytes(charities[charityId].name).length > 0,
            "Charity not found."
        );
        require(
            charities[charityId].verified,
            "Charity is not verified."
        );
        require(msg.value > 0, "Donation amount must be positive.");
        require(bytes(donorName).length > 0, "Donor name is required.");

        // ── Update balance ────────────────────────────────────
        charities[charityId].balance += msg.value;
        totalDonated                 += msg.value;
        totalDonationCount           += 1;

        // ── Emit event (replaces blockchain.add_transaction) ──
        emit DonationReceived(
            charityId,
            charities[charityId].name,
            msg.sender,
            donorName,
            msg.value,
            message,
            "RECEIVED"
        );
    }

    /**
     * @notice Admin releases funds to a verified beneficiary.
     * @dev    Equivalent to release_funds() in smart_contract.py.
     *         onlyOwner modifier mirrors the Python admin check.
     */
    function releaseFunds(
        string calldata charityId,
        string calldata beneficiaryId,
        uint256 amount
    ) external onlyOwner {

        require(
            bytes(charities[charityId].name).length > 0,
            "Charity not found."
        );
        require(
            bytes(beneficiaries[beneficiaryId].name).length > 0,
            "Beneficiary not found."
        );
        require(
            beneficiaries[beneficiaryId].verified,
            "Beneficiary not verified yet. Cannot release funds."
        );
        require(
            keccak256(bytes(beneficiaries[beneficiaryId].charityId)) ==
            keccak256(bytes(charityId)),
            "Beneficiary does not belong to this charity."
        );
        require(
            charities[charityId].balance >= amount,
            "Insufficient charity balance."
        );

        // ── Update balances ───────────────────────────────────
        charities[charityId].balance                -= amount;
        beneficiaries[beneficiaryId].fundsReceived  += amount;
        totalReleased                               += amount;

        // ── Transfer ETH to beneficiary's charity wallet ──────
        address payable wallet = payable(charities[charityId].wallet);
        wallet.transfer(amount);

        // ── Emit event ────────────────────────────────────────
        emit FundsReleased(
            charityId,
            charities[charityId].name,
            beneficiaryId,
            beneficiaries[beneficiaryId].name,
            amount,
            "DELIVERED"
        );
    }

    /**
     * @notice Admin approves a beneficiary (fraud check).
     * @dev    Equivalent to verify_beneficiary() in smart_contract.py.
     */
    function verifyBeneficiary(string calldata beneficiaryId)
        external
        onlyOwner
    {
        require(
            bytes(beneficiaries[beneficiaryId].name).length > 0,
            "Beneficiary not found."
        );

        beneficiaries[beneficiaryId].verified = true;

        emit BeneficiaryVerified(
            beneficiaryId,
            beneficiaries[beneficiaryId].name,
            "VERIFIED"
        );
    }

    /**
     * @notice Register a new beneficiary — starts unverified.
     * @dev    Equivalent to add_beneficiary() in smart_contract.py.
     *         Must be approved by admin before funds can be released.
     */
    function addBeneficiary(
        string calldata name,
        string calldata charityId
    ) external onlyOwner {

        require(
            bytes(charities[charityId].name).length > 0,
            "Charity not found."
        );

        // Generate a new beneficiary ID (mirrors Python's B001, B002 pattern)
        string memory newId = string(
            abi.encodePacked("B", _uint2str(beneficiaryIds.length + 1))
        );

        beneficiaries[newId] = Beneficiary({
            name:          name,
            charityId:     charityId,
            verified:      false,
            fundsReceived: 0
        });
        beneficiaryIds.push(newId);

        emit BeneficiaryAdded(newId, name, charityId);
    }

    // ── Read-only helpers (mirrors Python get_* functions) ────

    /**
     * @notice Returns key stats — mirrors get_stats() in Python.
     */
    function getStats() external view returns (
        uint256 _totalDonated,
        uint256 _totalReleased,
        uint256 _totalDonations,
        uint256 _chainLength,        // beneficiaryIds count as proxy
        bool    _chainValid          // always true in Solidity (immutable ledger)
    ) {
        return (
            totalDonated,
            totalReleased,
            totalDonationCount,
            beneficiaryIds.length,
            true
        );
    }

    /**
     * @notice Returns charity details by ID.
     */
    function getCharity(string calldata id)
        external
        view
        returns (
            string  memory name,
            address wallet,
            bool    verified,
            uint256 balance
        )
    {
        Charity memory c = charities[id];
        return (c.name, c.wallet, c.verified, c.balance);
    }

    /**
     * @notice Returns beneficiary details by ID.
     */
    function getBeneficiary(string calldata id)
        external
        view
        returns (
            string  memory name,
            string  memory charityId,
            bool    verified,
            uint256 fundsReceived
        )
    {
        Beneficiary memory b = beneficiaries[id];
        return (b.name, b.charityId, b.verified, b.fundsReceived);
    }

    /**
     * @notice Returns all registered charity IDs.
     */
    function getAllCharityIds() external view returns (string[] memory) {
        return charityIds;
    }

    /**
     * @notice Returns all registered beneficiary IDs.
     */
    function getAllBeneficiaryIds() external view returns (string[] memory) {
        return beneficiaryIds;
    }

    // ── Internal utility ──────────────────────────────────────

    function _uint2str(uint256 v) internal pure returns (string memory) {
        if (v == 0) return "0";
        uint256 temp = v;
        uint256 digits;
        while (temp != 0) { digits++; temp /= 10; }
        bytes memory buffer = new bytes(digits);
        while (v != 0) {
            digits--;
            buffer[digits] = bytes1(uint8(48 + (v % 10)));
            v /= 10;
        }
        return string(buffer);
    }

    // ── Fallback: accept plain ETH transfers ─────────────────
    receive() external payable {}
}
