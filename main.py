import tkinter as tk
from tkinter import messagebox, ttk
from atm import ATM
import json
from functools import partial

# Modern UI constants
COLORS = {
    'bg_dark': '#212529',         # Dark background
    'bg_medium': '#343a40',       # Medium background
    'accent': '#6c757d',          # Accent color
    'text_light': '#f8f9fa',      # Light text color
    'success': '#228B22',         # Dark green for success
    'primary': '#0062cc',         # Dark blue for primary actions
    'danger': '#dc3545',          # Red for dangerous actions
    'warning': '#ffc107',         # Yellow for warnings
    'info': '#17a2b8',            # Cyan for info
    'muted': '#6c757d'            # Muted gray
}

# Create a custom style for widgets
def create_button(parent, text, command, bg_color=COLORS['primary'], fg_color=COLORS['text_light'], width=15, height=2):
    """Create a modern styled button"""
    button = tk.Button(
        parent, 
        text=text, 
        command=command,
        font=('Helvetica', 12),
        width=width,
        height=height,
        bg=bg_color,
        fg=fg_color,
        activebackground=bg_color,
        activeforeground=fg_color,
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
        padx=10,
        pady=5
    )
    # Hover effect
    button.bind("<Enter>", lambda e: e.widget.config(bg=_adjust_lightness(bg_color, 1.1)))
    button.bind("<Leave>", lambda e: e.widget.config(bg=bg_color))
    return button

def create_entry(parent, show=None, width=20):
    """Create a modern styled entry field"""
    entry = tk.Entry(
        parent,
        font=('Helvetica', 12),
        width=width,
        bg=COLORS['bg_medium'],
        fg=COLORS['text_light'],
        insertbackground=COLORS['text_light'],  # Cursor color
        relief=tk.FLAT,
        highlightthickness=1,
        highlightcolor=COLORS['primary'],
        highlightbackground=COLORS['accent']
    )
    if show:
        entry.config(show=show)
    return entry

def create_label(parent, text, size=12, bold=False, fg=COLORS['text_light'], bg=COLORS['bg_dark']):
    """Create a modern styled label"""
    font_style = 'bold' if bold else 'normal'
    return tk.Label(
        parent,
        text=text,
        font=('Helvetica', size, font_style),
        fg=fg,
        bg=bg
    )

def create_frame(parent, padding_x=10, padding_y=10):
    """Create a modern styled frame"""
    return tk.Frame(
        parent,
        bg=COLORS['bg_dark'],
        padx=padding_x,
        pady=padding_y
    )

def _adjust_lightness(color, factor):
    """Adjust the lightness of a hex color"""
    # Simple lightness adjustment - not for production use
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    
    return f'#{r:02x}{g:02x}{b:02x}'

class ATMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Simulator")
        self.atm = ATM()
        
        # Configure full screen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Create main container with modern styling
        self.main_frame = create_frame(self.root, padding_x=30, padding_y=30)
        self.main_frame.pack(expand=True, fill='both')
        
        # Add ESC key binding to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Reference to balance display label
        self.balance_label = None
        
        # Create and show login frame
        self.create_login_frame()
        
    def create_login_frame(self):
        """Create the login screen with modern styling"""
        self.clear_frame()
        
        # Header container with logo effect
        header_frame = create_frame(self.main_frame)
        header_frame.pack(pady=(20, 40))
        
        # Title with modern styling
        title_label = create_label(header_frame, "BANK ATM TERMINAL", size=28, bold=True)
        title_label.pack()
        
        # Subtitle
        subtitle_label = create_label(header_frame, "Secure Banking Services", size=14, fg=COLORS['accent'])
        subtitle_label.pack(pady=(5, 0))
        
        # Login container with card-like effect
        login_container = tk.Frame(
            self.main_frame,
            bg=COLORS['bg_medium'],
            padx=40,
            pady=40,
            highlightbackground=COLORS['accent'],
            highlightthickness=1
        )
        login_container.pack(padx=100, pady=10)
        
        # Account Entry
        account_label = create_label(login_container, "Account Number:", bg=COLORS['bg_medium'])
        account_label.pack(anchor='w', pady=(0, 5))
        
        self.account_entry = create_entry(login_container, width=20)
        self.account_entry.pack(pady=(0, 15), fill='x')
        
        # PIN Entry
        pin_label = create_label(login_container, "Enter PIN:", bg=COLORS['bg_medium'])
        pin_label.pack(anchor='w', pady=(0, 5))
        
        self.pin_entry = create_entry(login_container, show="•", width=20)
        self.pin_entry.pack(pady=(0, 25), fill='x')
        
        # Button container
        button_frame = tk.Frame(login_container, bg=COLORS['bg_medium'])
        button_frame.pack(pady=(10, 0), fill='x')
        
        # Login Button
        login_button = tk.Button(
            button_frame, 
            text="LOGIN",
            command=self.login,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['primary'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        login_button.pack(side=tk.LEFT, padx=(0, 10))
        login_button.bind("<Enter>", lambda e, c=COLORS['primary']: e.widget.config(bg=c, fg='white'))
        login_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Register Button
        register_button = tk.Button(
            button_frame, 
            text="REGISTER",
            command=self.show_registration_dialog,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['info'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        register_button.pack(side=tk.LEFT, padx=10)
        register_button.bind("<Enter>", lambda e, c=COLORS['info']: e.widget.config(bg=c, fg='white'))
        register_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Exit Button
        exit_button = tk.Button(
            button_frame, 
            text="EXIT",
            command=self.root.quit,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['danger'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        exit_button.pack(side=tk.LEFT, padx=10)
        exit_button.bind("<Enter>", lambda e, c=COLORS['danger']: e.widget.config(bg=c, fg='white'))
        exit_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Footer
        footer_frame = create_frame(self.main_frame)
        footer_frame.pack(side=tk.BOTTOM, fill='x', pady=20)
        
        footer_text = create_label(
            footer_frame, 
            "© 2025 Modern Banking ATM • Made by Charu , Nandini , Anuj & Aashutosh", 
            size=10, 
            fg=COLORS['accent']
        )
        footer_text.pack(side=tk.RIGHT, padx=20)
        
        # Focus on account entry
        self.account_entry.focus_set()
        
    def create_menu_frame(self):
        """Create the main menu screen with modern styling"""
        self.clear_frame()
        
        # Header with customer info
        header_frame = create_frame(self.main_frame)
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Add current time indicator (just for visual effect)
        time_label = create_label(header_frame, "Session Active", size=10, fg=COLORS['accent'])
        time_label.pack(side=tk.RIGHT, padx=10)
        
        # Customer welcome
        customer_name = self.atm.get_customer_name()
        name_label = create_label(header_frame, f"Welcome, {customer_name}", size=16, bold=True)
        name_label.pack(side=tk.LEFT, padx=10)
        
        # Balance display
        balance_frame = tk.Frame(
            self.main_frame,
            bg=COLORS['bg_medium'],
            padx=20,
            pady=15
        )
        balance_frame.pack(fill='x', pady=(0, 30))
        
        balance_label = create_label(
            balance_frame, 
            "Current Balance", 
            size=12, 
            fg=COLORS['accent'],
            bg=COLORS['bg_medium']
        )
        balance_label.pack()
        
        # Store reference to the balance amount label for updates
        self.balance_label = create_label(
            balance_frame, 
            f"\u20B9 {self.atm.check_balance():.2f}", 
            size=24, 
            bold=True,
            bg=COLORS['bg_medium']
        )
        self.balance_label.pack()
        
        # Menu container
        menu_container = create_frame(self.main_frame)
        menu_container.pack(expand=True, fill='both')
        
        # Create a grid for menu options
        menu_items = [
            ("Deposit", self.deposit, COLORS['success']),
            ("Withdraw", self.withdraw, COLORS['primary']),
            ("Transaction History", self.show_history, COLORS['info']),
            ("Change PIN", self.change_pin, COLORS['warning']),
            ("Logout", self.logout, COLORS['danger']),
            ("Exit ATM", self.root.quit, COLORS['muted'])
        ]
        
        # Create card-like containers for each menu option
        for i, (text, command, color) in enumerate(menu_items):
            row, col = divmod(i, 3)
            
            # Create a card-like container
            card_frame = tk.Frame(
                menu_container,
                bg=COLORS['bg_medium'],
                padx=20,
                pady=20,
                highlightbackground=color,
                highlightthickness=2
            )
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Create card content container for better organization
            content_frame = tk.Frame(card_frame, bg=COLORS['bg_medium'])
            content_frame.pack(fill='both', expand=True)
            
            # Header container
            header_frame = tk.Frame(content_frame, bg=COLORS['bg_medium'])
            header_frame.pack(fill='x', anchor='nw')
            
            # Add icon placeholder (simple colored square for now)
            icon = tk.Frame(header_frame, bg=color, width=30, height=30)
            icon.pack(side=tk.LEFT, pady=(0, 10))
            
            # Option name - place next to icon
            option_name = create_label(header_frame, text, size=16, bold=True, bg=COLORS['bg_medium'])
            option_name.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
            
            # Make the entire card clickable - add a button that fills most of the space
            action_button = tk.Button(
                content_frame,
                text="SELECT",
                command=command,
                font=('Helvetica', 12, 'bold'),
                bg='white',  # High contrast button
                fg=COLORS['bg_dark'],  # Dark text for contrast
                activebackground=color,
                activeforeground='white',
                relief=tk.RAISED,  # Give it a raised appearance
                borderwidth=2,
                padx=10,
                pady=5,
                width=15,  # Make button wider
                height=2,   # Make button taller
                cursor="hand2"  # Change cursor to hand when hovering
            )
            action_button.pack(side=tk.BOTTOM, fill='x', pady=(15, 0))
            
            # Add hover effect to the button
            action_button.bind("<Enter>", lambda e, c=color: e.widget.config(bg=c, fg='white'))
            action_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
            
            # Make the entire card feel clickable by changing cursor on hover
            for widget in [card_frame, content_frame, header_frame, option_name, icon]:
                widget.bind("<Enter>", lambda e, b=action_button, c=color: b.config(bg=c, fg='white'))
                widget.bind("<Leave>", lambda e, b=action_button: b.config(bg='white', fg=COLORS['bg_dark']))
        
        # Configure grid to be responsive
        for i in range(3):
            menu_container.columnconfigure(i, weight=1)
        menu_container.rowconfigure(0, weight=1)
        menu_container.rowconfigure(1, weight=1)
        
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def login(self):
        """Handle login with full account number"""
        full_account = self.account_entry.get()
        pin = self.pin_entry.get()
        
        success, message = self.atm.login(full_account, pin)
        if success:
            self.create_menu_frame()
        else:
            if "Please register" in message:
                response = messagebox.askyesno("Account Not Found", 
                    f"{message}\nWould you like to register a new account?")
                if response:
                    self.show_registration_dialog(full_account)
            else:
                messagebox.showerror("Login Failed", message)
                if "locked" in message:
                    self.root.quit()
                    
    def show_registration_dialog(self, account_number=""):
        """Show registration dialog for new users with modern styling"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Account Registration")
        dialog.geometry("450x520")
        dialog.configure(bg=COLORS['bg_dark'])
        
        # Add some padding
        container = create_frame(dialog, padding_x=25, padding_y=25)
        container.pack(fill='both', expand=True)
        
        # Title
        title = create_label(container, "Create New Account", size=18, bold=True)
        title.pack(pady=(0, 20))
        
        # Form fields
        # Account Number
        account_label = create_label(container, "Account Number:")
        account_label.pack(anchor='w', pady=(0, 5))
        
        account_entry = create_entry(container)
        account_entry.pack(fill='x', pady=(0, 15))
        if account_number:
            account_entry.insert(0, account_number)
            account_entry.config(state='readonly')
        
        # Name
        name_label = create_label(container, "Full Name:")
        name_label.pack(anchor='w', pady=(0, 5))
        
        name_entry = create_entry(container)
        name_entry.pack(fill='x', pady=(0, 15))
        
        # PIN
        pin_label = create_label(container, "Create 4-digit PIN:")
        pin_label.pack(anchor='w', pady=(0, 5))
        
        pin_entry = create_entry(container, show="•")
        pin_entry.pack(fill='x', pady=(0, 15))
        
        # Initial Deposit
        deposit_label = create_label(container, "Initial Deposit:")
        deposit_label.pack(anchor='w', pady=(0, 5))
        
        deposit_entry = create_entry(container)
        deposit_entry.pack(fill='x', pady=(0, 15))
        deposit_entry.insert(0, "0")
        
        # Status message
        status_label = create_label(container, "", fg=COLORS['warning'])
        status_label.pack(pady=10)
        
        def register():
            full_account = account_entry.get()
            name = name_entry.get()
            pin = pin_entry.get()
            
            try:
                deposit = float(deposit_entry.get())
                if deposit < 0:
                    raise ValueError
            except ValueError:
                status_label.config(text="Invalid deposit amount")
                return
            
            # Check if account already exists
            if full_account in self.atm.accounts:
                status_label.config(text="Account already registered!")
                return
                
            if not name.strip():
                status_label.config(text="Name cannot be empty")
                return
                
            if len(pin) != 4 or not pin.isdigit():
                status_label.config(text="PIN must be 4 digits")
                return
                
            success, message = self.atm.register_user(
                full_account, name, pin, deposit
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                # Auto-login the new user
                self.atm.login(full_account, pin)
                self.create_menu_frame()
            else:
                status_label.config(text=message)
        
        # Button container
        button_frame = create_frame(container, padding_x=0, padding_y=0)
        button_frame.pack(pady=10)
        
        # Register button
        register_button = tk.Button(
            button_frame, 
            text="REGISTER",
            command=register,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['success'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        register_button.pack(side=tk.LEFT, padx=10)
        register_button.bind("<Enter>", lambda e, c=COLORS['success']: e.widget.config(bg=c, fg='white'))
        register_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame, 
            text="CANCEL",
            command=dialog.destroy,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['danger'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        cancel_button.bind("<Enter>", lambda e, c=COLORS['danger']: e.widget.config(bg=c, fg='white'))
        cancel_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
    def logout(self):
        """Handle logout"""
        self.atm.logout()
        self.create_login_frame()
        
    def check_balance(self):
        """Show current balance"""
        balance = self.atm.check_balance()
        messagebox.showinfo("Account Balance", 
                          f"Current Balance: \u20B9 {balance:.2f}")
        
    def update_balance_display(self):
        """Update the balance display in the main menu"""
        if hasattr(self, 'balance_label') and self.balance_label:
            self.balance_label.config(text=f"\u20B9 {self.atm.check_balance():.2f}")
        
    def deposit(self):
        """Handle deposit"""
        amount = self.get_amount("Enter deposit amount:")
        if amount is not None:
            if self.atm.deposit(amount):
                messagebox.showinfo("Deposit Successful", 
                                 f"\u20B9 {amount:.2f} deposited successfully.\nNew Balance: \u20B9 {self.atm.check_balance():.2f}")
                # Update the balance display
                self.update_balance_display()
            else:
                messagebox.showerror("Error", "Invalid deposit amount!")
                
    def withdraw(self):
        """Handle withdrawal"""
        amount = self.get_amount("Enter withdrawal amount:")
        if amount is not None:
            if self.atm.withdraw(amount):
                messagebox.showinfo("Withdrawal Successful", 
                                   f"\u20B9 {amount:.2f} withdrawn successfully.\nNew Balance: \u20B9 {self.atm.check_balance():.2f}")
                # Update the balance display
                self.update_balance_display()
            else:
                messagebox.showerror("Error", "Invalid amount or insufficient funds!")
                
    def change_pin(self):
        """Handle PIN change with modern styling"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Change PIN")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS['bg_dark'])
        
        # Container
        container = create_frame(dialog, padding_x=25, padding_y=25)
        container.pack(fill='both', expand=True)
        
        # Title
        title = create_label(container, "Change Your PIN", size=18, bold=True)
        title.pack(pady=(0, 20))
        
        # Old PIN
        old_pin_label = create_label(container, "Current PIN:")
        old_pin_label.pack(anchor='w', pady=(0, 5))
        
        old_pin_entry = create_entry(container, show="•")
        old_pin_entry.pack(fill='x', pady=(0, 15))
        
        # New PIN
        new_pin_label = create_label(container, "New 4-digit PIN:")
        new_pin_label.pack(anchor='w', pady=(0, 5))
        
        new_pin_entry = create_entry(container, show="•")
        new_pin_entry.pack(fill='x', pady=(0, 15))
        
        # Confirm New PIN
        confirm_pin_label = create_label(container, "Confirm New PIN:")
        confirm_pin_label.pack(anchor='w', pady=(0, 5))
        
        confirm_pin_entry = create_entry(container, show="•")
        confirm_pin_entry.pack(fill='x', pady=(0, 15))
        
        def confirm():
            old_pin = old_pin_entry.get()
            new_pin = new_pin_entry.get()
            confirm_pin = confirm_pin_entry.get()
            
            if new_pin != confirm_pin:
                messagebox.showerror("Error", "New PINs don't match!")
                return
                
            if self.atm.change_pin(old_pin, new_pin):
                messagebox.showinfo("Success", "PIN changed successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid current PIN or new PIN must be 4 digits!")
        
        # Confirm button
        confirm_button = tk.Button(
            container, 
            text="CONFIRM",
            command=confirm,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['success'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        confirm_button.pack(pady=20)
        confirm_button.bind("<Enter>", lambda e, c=COLORS['success']: e.widget.config(bg=c, fg='white'))
        confirm_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
    def show_history(self):
        """Show transaction history with modern styling"""
        history = self.atm.get_transaction_history()
        if not history:
            messagebox.showinfo("Transaction History", "No transactions found")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Transaction History")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS['bg_dark'])
        
        # Container
        container = create_frame(dialog, padding_x=25, padding_y=25)
        container.pack(fill='both', expand=True)
        
        # Title
        title = create_label(container, "Recent Transactions", size=18, bold=True)
        title.pack(pady=(0, 20))
        
        # Create custom style for treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', 
                        background=COLORS['bg_medium'],
                        foreground=COLORS['text_light'],
                        rowheight=25,
                        fieldbackground=COLORS['bg_medium'])
        style.configure('Treeview.Heading', 
                        background=COLORS['accent'],
                        foreground=COLORS['text_light'],
                        font=('Helvetica', 10, 'bold'))
        style.map('Treeview', background=[('selected', COLORS['primary'])])
        
        # Transaction list
        tree_frame = tk.Frame(container, bg=COLORS['bg_dark'])
        tree_frame.pack(fill='both', expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=('Date', 'Transaction'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Transaction', text='Transaction')
        tree.column('Date', width=150)
        tree.column('Transaction', width=350)
        
        for i, transaction in enumerate(reversed(history)):
            # Add date as first column (placeholder)
            parts = transaction.split(' - ')
            date = parts[0] if len(parts) > 1 else "Today"
            details = parts[1] if len(parts) > 1 else transaction
            tree.insert('', 'end', values=(date, details))
            
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Close button
        close_button = tk.Button(
            container, 
            text="CLOSE",
            command=dialog.destroy,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['accent'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        close_button.pack(pady=(20, 0))
        close_button.bind("<Enter>", lambda e, c=COLORS['accent']: e.widget.config(bg=c, fg='white'))
        close_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
    def get_amount(self, prompt):
        """Get amount from user with modern styling"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Amount Entry")
        dialog.geometry("400x250")
        dialog.configure(bg=COLORS['bg_dark'])
        
        # Container
        container = create_frame(dialog, padding_x=25, padding_y=25)
        container.pack(fill='both', expand=True)
        
        # Prompt
        prompt_label = create_label(container, prompt, size=14)
        prompt_label.pack(pady=15)
        
        # Amount entry
        amount_entry = create_entry(container, width=20)
        amount_entry.pack(pady=15)
        amount_entry.focus_set()
        
        amount = None
        
        def confirm():
            nonlocal amount
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive amount!")
                
        # Button container
        button_frame = create_frame(container, padding_x=0, padding_y=0)
        button_frame.pack(pady=10)
        
        # Confirm button
        confirm_button = tk.Button(
            button_frame, 
            text="CONFIRM",
            command=confirm,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['success'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        confirm_button.pack(side=tk.LEFT, padx=10)
        confirm_button.bind("<Enter>", lambda e, c=COLORS['success']: e.widget.config(bg=c, fg='white'))
        confirm_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame, 
            text="CANCEL",
            command=dialog.destroy,
            font=('Helvetica', 12, 'bold'),
            bg='white',
            fg=COLORS['bg_dark'],
            activebackground=COLORS['danger'],
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            pady=5,
            width=10,
            height=2,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        cancel_button.bind("<Enter>", lambda e, c=COLORS['danger']: e.widget.config(bg=c, fg='white'))
        cancel_button.bind("<Leave>", lambda e: e.widget.config(bg='white', fg=COLORS['bg_dark']))
        
        # Make dialog modal
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return amount

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMGUI(root)
    root.mainloop()