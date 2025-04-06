# Banking ATM Simulator

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A modern ATM Simulator with a sleek graphical user interface built using Python and Tkinter. This application accurately simulates real-world banking operations with secure authentication and core banking functionalities.

![ATM Simulator Screenshot](screenshots/screenshot.png)

## 🌟 Features

- **Modern User Interface**: Clean design with intuitive navigation
- **Secure Authentication**: PIN-based login system
- **Core Banking Operations**:
  - Balance Inquiry
  - Cash Deposits
  - Cash Withdrawals
  - PIN Management
  - Transaction History
- **User Management**: Register new accounts with initial deposits
- **Data Persistence**: All user data and transactions are saved in JSON format
- **Responsive Design**: Full-screen operation with elegant styling

## 🚀 Getting Started

### Prerequisites

- Python 3.x (No external dependencies needed as Tkinter is included in standard Python)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/banking-atm-simulator.git
   cd banking-atm-simulator
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## 💻 Usage

### Login with Default Accounts

Use one of these test accounts:

- **Account 1**: 10001234 (PIN: 1234)
- **Account 2**: 20005678 (PIN: 5678)

### Create a New Account

1. Click on the "REGISTER" button on the login screen
2. Enter your details:
   - Full name
   - Account number
   - PIN (4 digits)
   - Initial deposit amount
3. Click "Register" to create your account

### ATM Operations

After logging in, you can:

- Check your balance
- Deposit funds
- Withdraw cash
- View transaction history
- Change your PIN
- Logout securely

## 🏗️ Project Structure

```
banking-atm-simulator/
├── main.py           # Main application with GUI components
├── atm.py            # Core ATM business logic
├── users.json        # User data storage
└── requirements.txt  # Project dependencies
```

## 🧠 Architecture

The project follows a clean separation between business logic and presentation:

1. **Backend Logic (`atm.py`)**:

   - Handles all banking operations and data management
   - Manages user authentication and security
   - Processes transactions and updates account balances
   - Maintains transaction history

2. **Frontend Interface (`main.py`)**:

   - Implements the responsive GUI with Tkinter
   - Provides visual feedback for user actions
   - Validates user inputs before processing
   - Renders transaction details and account information

3. **Data Store (`users.json`)**:
   - Persists user account information
   - Stores transaction records
   - Maintains system state between sessions

## 🔒 Security Note

This is a simulation project for educational purposes. In a production environment, additional security measures would be implemented:

- Encrypted data storage
- Secure authentication protocols
- Database integration
- Comprehensive logging
- Session management
- Input validation and sanitization

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/banking-atm-simulator/issues).

## 🙏 Acknowledgements

- Python and Tkinter documentation
- Modern UI design principles
- Banking security best practices
