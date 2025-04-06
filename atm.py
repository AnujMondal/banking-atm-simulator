import json
from datetime import datetime
import os

class ATM:
    def __init__(self):
        self.current_account = None
        self.pin_attempts = 0
        self.max_pin_attempts = 3
        self.accounts_file = "users.json"
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        """Load accounts from JSON file or create default if not exists"""
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    # Check if file is empty
                    if os.stat(self.accounts_file).st_size == 0:
                        return self._create_default_accounts()
                    return json.load(f)
            except json.JSONDecodeError:
                # If JSON is invalid, create default accounts
                return self._create_default_accounts()
        else:
            return self._create_default_accounts()

    def _create_default_accounts(self):
        """Create default accounts and save to file"""
        default_accounts = {
            "10001234": {
                "pin": "1234",
                "balance": 1000.0,
                "name": "John Doe",
                "transaction_history": []
            },
            "20005678": {
                "pin": "5678",
                "balance": 2500.0,
                "name": "Jane Smith",
                "transaction_history": []
            }
        }
        self._save_accounts(default_accounts)
        return default_accounts

    def _save_accounts(self, accounts=None):
        """Save accounts to JSON file"""
        with open(self.accounts_file, 'w') as f:
            json.dump(accounts or self.accounts, f, indent=4)

    def get_all_users(self):
        """Return all registered users"""
        return self.accounts

    def register_user(self, full_account, name, pin, initial_deposit=0):
        """Register a new user"""
        if full_account in self.accounts:
            return False, "Account already exists"
        
        if len(pin) != 4 or not pin.isdigit():
            return False, "PIN must be 4 digits"
        
        if initial_deposit < 0:
            return False, "Initial deposit cannot be negative"
        
        self.accounts[full_account] = {
            "pin": pin,
            "balance": float(initial_deposit),
            "name": name,
            "transaction_history": [f"Account created with initial deposit: ${initial_deposit:.2f}"]
        }
        
        self._save_accounts()
        return True, "Registration successful"

    def login(self, full_account, pin):
        """Authenticate user with full account number and PIN"""
        if self.pin_attempts >= self.max_pin_attempts:
            return False, "Too many attempts. Account locked."
            
        if full_account in self.accounts:
            if pin == self.accounts[full_account]["pin"]:
                self.current_account = full_account
                self.pin_attempts = 0
                self._add_transaction("Login")
                return True, "Login successful"
            else:
                self.pin_attempts += 1
                remaining = self.max_pin_attempts - self.pin_attempts
                return False, f"Invalid PIN. {remaining} attempts remaining."
        return False, "Account not found. Please register."

    def logout(self):
        """Logout the current user"""
        if self.current_account:
            self._add_transaction("Logout")
        self.current_account = None
        return True

    def check_balance(self):
        """Return current balance"""
        if self.current_account:
            balance = self.accounts[self.current_account]["balance"]
            self._add_transaction("Balance Check")
            return balance
        return None

    def deposit(self, amount):
        """Deposit money into account"""
        if self.current_account and amount > 0:
            self.accounts[self.current_account]["balance"] += amount
            self._add_transaction(f"Deposit: ${amount:.2f}")
            self._save_accounts()
            return True
        return False

    def withdraw(self, amount):
        """Withdraw money from account"""
        if (self.current_account and amount > 0 and 
            amount <= self.accounts[self.current_account]["balance"]):
            self.accounts[self.current_account]["balance"] -= amount
            self._add_transaction(f"Withdrawal: ${amount:.2f}")
            self._save_accounts()
            return True
        return False

    def change_pin(self, old_pin, new_pin):
        """Change PIN if old PIN is correct"""
        if (self.current_account and 
            old_pin == self.accounts[self.current_account]["pin"] and 
            len(new_pin) == 4 and new_pin.isdigit()):
            self.accounts[self.current_account]["pin"] = new_pin
            self._add_transaction("PIN Changed")
            self._save_accounts()
            return True
        return False

    def get_transaction_history(self):
        """Get last 5 transactions"""
        if self.current_account:
            return self.accounts[self.current_account]["transaction_history"][-5:]
        return []

    def get_customer_name(self):
        """Get current customer name"""
        if self.current_account:
            return self.accounts[self.current_account]["name"]
        return ""

    def _add_transaction(self, transaction_type):
        """Add transaction to history"""
        if self.current_account:
            self.accounts[self.current_account]["transaction_history"].append(
                f"{transaction_type} at {self._get_current_time()}"
            )

    def _get_current_time(self):
        """Helper to get current time string"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_authenticated(self):
        """Check if user is logged in"""
        return self.current_account is not None