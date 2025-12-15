import sqlite3
from sqlite3 import connect    # import libraray

conn=sqlite3.connect('atm.db')     # अगर यह file पहले से मौजूद है → उसी से connect करेगा।
                                    # अगर file मौजूद नहीं है → नई database file बना देगा उसी नाम से
 
print(conn)     # database print karata hai

cur=conn.cursor() # object created....   cuesor वो object है जो database से query execute करता है .



# ---------------------------
# Initialize Database
# ---------------------------

def init_db():
    conn=sqlite3.connect('atm.db')
    cur = conn.cursor()
                                                      # execute command sql query run karata hai .  
    cur.execute('''                                        
        CREATE TABLE IF NOT EXISTS accounts(
            acc_no int not null primary key,
            name varchar(20) NOT NULL,
            bank_name varchar(20) not null,
            balance float NOT NULL
        ) ''')         # table created
    
    conn.commit()      # Database में किए गए changes permanent कर देता है।
                       # बिना commit के changes सिर्फ memory में रहते हैं

    conn.close()       # Connection बंद कर देता है |


    conn=sqlite3.connect('atm.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_no int NOT NULL,
            type varchar(20) NOT NULL,              -- Deposit / Withdraw
            amount FLOAT NOT NULL,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(acc_no) REFERENCES accounts(acc_no)
        )
    ''')

    conn.commit()
    conn.close()


# ---------------------------
# Create Account
# ---------------------------
def create_account(acc_no, name,bank_name, balance):
    conn = sqlite3.connect('atm.db')
    cur = conn.cursor()
    
    try:
        cur.execute('''
            INSERT INTO accounts(acc_no, name,bank_name,balance)
            VALUES (?, ?, ?, ?)
        ''', (acc_no, name,bank_name,balance))
        conn.commit()
        print("✅ Account created successfully!")
    except sqlite3.IntegrityError:
        print("❌ Account already exists!")
    finally:
        conn.close()

# ---------------------------
# Check Balance
# ---------------------------
def check_balance(acc_no):
    conn = sqlite3.connect('atm.db')
    cur = conn.cursor()
    try:
       cur.execute("SELECT balance FROM accounts WHERE acc_no = ? ", (acc_no,))
       row = cur.fetchone()

       if row:
           return row[0]
       else:
           print("Account not found!")
    finally:
        conn.close()
 
# ---------------------------
# Deposit Money
# ---------------------------
def deposit(acc_no, amount):
    if amount <= 0:
        print("❌ Invalid deposit amount.")
        return
    
    conn = sqlite3.connect('atm.db')
    cur = conn.cursor()

    try:

       cur.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc_no,))
       row = cur.fetchone()

       if not row:
           print("❌ Account not found!")
           conn.close()
           return

       new_balance = row[0] + amount
       cur.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?",
                (new_balance,acc_no))
       conn.commit()

       print(f"💰 Deposit successful! New Balance: Rs. {new_balance}")
       transaction(acc_no ,"Deposit", amount)


    finally:
        conn.close()


# ---------------------------
# Withdraw Money
# ---------------------------
def withdraw(acc_no, amount):
    if amount <= 0:
        print("❌ Invalid withdrawal amount.")
        return

    conn = sqlite3.connect("atm.db")
    cur = conn.cursor()
     
    try:  
        cur.execute("SELECT balance FROM accounts WHERE acc_no = ?", (acc_no,))
        row = cur.fetchone()

        if not row:
            print("❌ Account not found!")
            return

        balance = row[0]

        if amount > balance:
            print("❌ Insufficient balance.")
            return

        new_balance = balance - amount
        cur.execute("UPDATE accounts SET balance = ? WHERE acc_no = ?",(new_balance,acc_no))
        conn.commit()
  
        print(f"Withdrawal successful! Remaining Balance: Rs. {new_balance}")
        transaction(acc_no,"Withdraw", amount)

    finally:
        conn.close()


# ---------------------------
# Transcition
# ---------------------------

def transaction(acc_no,type, amount):
    conn = sqlite3.connect('atm.db')
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO transactions(acc_no,type, amount)
        VALUES (?, ?, ?)
        ''', (acc_no,type, amount))
    conn.commit()
    conn.close()


# ---------------------------
# view transaction
# ---------------------------

def view_transactions(acc_no):
    conn = sqlite3.connect('atm.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT transaction_id, type, amount, time FROM transactions
        WHERE acc_no = ?
        ORDER BY time ASC
        LIMIT 10
    """, (acc_no,))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    print("\nTransaction History (Last 10):")
    print("-" * 40)
    for txn in rows:
        print(f"TransactionID: {txn[0]} | {txn[1]} Rs.{txn[2]} | {txn[3]}")
    print("-" * 40)

# ---------------------------
# MAIN PROGRAM
# ---------------------------



init_db()

while True:

    print("ATM")
    print("1. Create account")
    print("2. Check balance")
    print("3. Withdraw")
    print("4. Deposit")
    print("5. Tranactions")
    print("6. Exit")

    ch = int(input("\nEnter your choice (1-6): "))

    if ch == 1:
        acc_no = int(input("Enter account number: "))
        name = input("Enter your name: ")
        bank_name=input("Enter bank name: ")
        bal = float(input("Enter initial balance: "))
        create_account(acc_no, name,bank_name,bal)

    elif ch == 2:
        acc_no = int(input("Enter account number: "))
        bal = check_balance(acc_no)
        if bal is not None:
            print(f"Your balance is: Rs. {bal}")

    elif ch == 3:
        acc_no = int(input("Enter account number: "))
        amt = float(input("Enter amount to withdraw: "))
        withdraw(acc_no, amt)

    elif ch == 4:
        acc_no = int(input("Enter account number: "))
        amt = float(input("Enter amount to deposit: "))
        deposit(acc_no, amt)

    elif ch == 5:
        acc_no = int(input("Enter account number: "))
        view_transactions(acc_no)

    elif ch == 6:
        print("Exiting... Goodbye!")
        break

    else:
        print("❌ Invalid choice! Please enter between 1–6.")