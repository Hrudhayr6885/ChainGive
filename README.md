# ============================================================
# README.md
# Charity Blockchain Platform - Main Documentation
# ============================================================

## 🎯 Project Overview

**Charity Blockchain Platform** is a secure, transparent donation management system built on blockchain technology. It uses advanced consensus mechanisms, role-based authentication, and fraud detection to ensure safe and transparent charity operations.

### Key Features
- ✅ **Blockchain-based** - Immutable transaction records
- ✅ **Proof-of-Work** - Secure mining with difficulty adjustment
- ✅ **Byzantine Fault Tolerance** - Consensus algorithm resilient to failures
- ✅ **Multi-Role Authentication** - Admin, Charity Manager, Donor roles
- ✅ **Fraud Detection** - Automatic flagging of suspicious transactions
- ✅ **Blockchain Explorer** - Real-time chain visualization
- ✅ **Audit Logging** - Complete audit trail of all actions

---

## 🏗️ Project Structure

```
Charity_BC_Final/
│
├── core/                              # Core Blockchain Logic (PERSON 1)
│   ├── blockchain.py                 # Block and chain implementation
│   ├── consensus.py                  # Byzantine consensus engine
│   ├── contract_logic.py              # Smart contract business logic
│   ├── auth.py                       # (PERSON 3) Authentication system
│   └── __init__.py
│
├── web/                              # Web Application (PERSON 2)
│   ├── app.py                        # Flask routes and handlers
│   ├── decorators.py                 # Auth decorators
│   └── __init__.py
│
├── templates/                        # HTML Templates
│   ├── base.html                     # Base template
│   ├── index.html                    # Home page
│   ├── login.html                    # Login page
│   ├── register.html                 # Registration page
│   ├── donate.html                   # Donation form
│   ├── track.html                    # Transaction tracking
│   ├── explorer.html                 # Blockchain explorer
│   ├── dashboard.html                # User dashboard
│   ├── admin.html                    # Admin panel
│   ├── admin_users.html              # User management
│   ├── settings.html                 # User settings
│   ├── 404.html                      # Error page
│   └── 500.html                      # Error page
│
├── contracts/                        # Smart Contract Reference
│   ├── smart_contract.sol            # Solidity contract (reference)
│   └── CONTRACT_NOTES.md             # Contract documentation
│
├── config.py                         # Configuration file
├── run.py                            # Main entry point
├── requirements.txt                  # Python dependencies
├── data.json                         # Persistent blockchain storage
├── README.md                         # This file
└── README_DEMO.md                    # Demo guide for 3-person team

---

## 👥 Team Roles

### Person 1 — Blockchain & Consensus Developer (core/blockchain.py + core/consensus.py + core/contract_logic.py)
- Connects the blockchain to the web interface
- Writes all URL routes: `/`, `/donate`, `/track`, `/explorer`, `/admin`
- Handles form submissions and flash messages
- Writes admin actions: release funds, verify beneficiary
- Provides `/api/chain` and `/api/stats` JSON endpoints

### Person 3 — Frontend / GUI (`templates/` folder)
- Designs all 5 HTML pages using Jinja2 templates:
  - `base.html` — navigation and shared layout
  - `index.html` — home page with stats and recent transactions
  - `donate.html` — donation form
  - `track.html` — search and view donation status
  - `explorer.html` — full blockchain block viewer
  - `admin.html` — admin panel for verification & fund release
- Makes the UI dark-themed, clean, and readable

---

## 📁 Project Structure

```
charity_blockchain/
├── blockchain.py        ← Person 1: Block + Blockchain classes
├── smart_contract.py    ← Person 1: Contract logic (donate, release, verify)
├── app.py               ← Person 2: Flask web server
├── templates/
│   ├── base.html        ← Person 3: Shared layout
│   ├── index.html       ← Person 3: Home page
│   ├── donate.html      ← Person 3: Donation form
│   ├── track.html       ← Person 3: Track donations
│   ├── explorer.html    ← Person 3: Blockchain explorer
│   └── admin.html       ← Person 3: Admin panel
└── requirements.txt
```

---

## 🚀 How to Run

### Step 1 — Make sure Python is installed
```bash
python --version   # should be 3.10 or newer
```

### Step 2 — Open a terminal and go to the project folder
```bash
cd charity_blockchain
```

### Step 3 — Install Flask (one-time setup)
```bash
pip install flask
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open your browser
Go to: **http://127.0.0.1:5000**

---

## 🖥️ Pages

| URL | What it does |
|-----|-------------|
| `/` | Home — stats, charities, recent transactions |
| `/donate` | Make a donation → recorded on blockchain |
| `/track` | Paste your hash to track your donation |
| `/explorer` | View every block in the chain |
| `/admin` | Verify beneficiaries, release funds |

---

## � Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone/Extract Project**
   ```bash
   cd /Users/hrudhayr/Downloads/Charity_BC_Final
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python run.py
   ```

4. **Access Application**
   - Open browser to: `http://127.0.0.1:8080`

---

## 🔐 Authentication

### User Roles

| Role | Permissions | Default User |
|------|-------------|--------------|
| **Admin** | All functions, user management, audit logs | Admin / Admin@123 |
| **Charity Manager** | Manage beneficiaries, view donations | Charity_Manager / Manager@123 |
| **Donor** | Make donations, track transactions | (Register new) |

### Default Accounts

```
Admin Account:
  Username: Admin
  Password: Admin@123

Manager Account:
  Username: Charity_Manager
  Password: Manager@123
```

---

## 📊 Demo Information

### What Each Person Can Demo

**See README_DEMO.md for detailed demo breakdowns:**

- **PERSON 1:** Blockchain core, consensus algorithm, fraud detection
- **PERSON 2:** Web application, all routes, user interface
- **PERSON 3:** Authentication, authorization, security, audit logging

---

## 🎓 Ready to Demo!

Your project is now properly structured for a professional 3-person team demo.

**Start the application:**
```bash
python run.py
```

Then visit: `http://127.0.0.1:8080`

**See README_DEMO.md for complete demo guide with timing and walkthrough.**

---

**Project Version:** 1.0.0
**Last Updated:** April 16, 2026
**Status:** ✅ Production Ready for Demo


1. Go to **http://127.0.0.1:5000** — see the home page with 3 verified charities
2. Click **Donate** → enter your name, pick a charity, enter ₹500, click Donate
3. You'll be redirected to **Track** with your block hash — see "RECEIVED" status
4. Go to **Admin** → find "Priya Nair" (unverified) → click **Verify**
5. Go to **Admin** → Release Funds → pick Health Aid Fund → pick Priya Nair → ₹300
6. Go to **Explorer** → see every block, hash, and transaction
7. Go to **Track** → paste the donation hash → see RECEIVED → DELIVERED status

---

## ⚙️ Key Concepts Explained

### Blockchain
Each donation creates a new **Block**. The block contains:
- The transaction data (who donated, how much, to which charity)
- A **SHA-256 hash** of the block's contents
- The **previous block's hash** (this is what chains them together)

If anyone tries to change a past donation, the hash changes, and the chain becomes invalid.

### Proof-of-Work
Before a block is accepted, the computer must find a `nonce` (random number)
that makes the hash start with "00". This makes it computationally expensive
to tamper with history.

### Smart Contract (in Python)
In real Solidity/Ethereum, a smart contract is code that runs on the blockchain.
Here, `smart_contract.py` mimics this: it contains the **rules** that control
donations — you can only release funds to a **verified** beneficiary, and only
if the charity has enough balance.

### Fraud Check
Beneficiaries are added as **unverified** by default. An admin must manually
approve them before any funds can be released. This step is recorded on-chain.

---

## 📊 Algorithms Used

1. **SHA-256 Hashing** — creates a unique fingerprint for each block
2. **Proof-of-Work** — ensures blocks can't be changed cheaply (difficulty = 2 leading zeros)
3. **Linked List + Hash Pointers** — each block stores the previous block's hash, forming a chain
4. **Chain Validation** — recalculates every hash to verify integrity
5. **Input Validation** — prevents negative donations, unverified beneficiaries, insufficient balance

---
