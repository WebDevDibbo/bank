from abc import ABC
import random



class Bank:
    def __init__(self,name) -> None:
        self.name = name
        self.account_list = []
        self.admin_list = []
        self.total_balance = 500000000
        self.total_loan = 0
        self.loan_status = True
        self.is_bankrupt = False

    def create_account(self,account):
        self.account_list.append(account)

    def find_account(self,account_no):
        for account in self.account_list:
            if account.account_number == account_no:
                return account
        return None
    
    def create_admin(self,account):
        self.admin_list.append(account)

    def find_admin_account(self,account_name):
        for acc in self.admin_list:
            if acc.name == account_name:
                return acc
        return None
    
    def delete_account(self,account_no):
        account = self.find_account(account_no)
        if account:
            self.account_list.remove(account)
            print("**** Account deleted Successfully ****")
        else:
            print("Account Not Found!!")

    def show_users(self):
        print("Account_No\tName\tEmail\tAddress\tBalance")
        for user in self.account_list:
            print(f"{user.account_number} {user.name} {user.email} {user.address} {user.balance}")

    def check_balance(self):
        print(f"Total Balance - {self.total_balance}")

    def check_loan(self):
        print(f"Total Loan - {self.total_loan}")
        return self.total_loan

    def loan_feature(self,select):
        if select == 1:
            self.loan_status == True
            print("loan feature is ON Successfully!")
        elif select == 2 :
            self.loan_status == False
            print("Loan feature is OFF Successfully!")
        else:
            print("Invalid!!")


class User(ABC):
    def __init__(self,name,email,address) -> None:
        self.name = name
        self.email = email
        self.address = address


class Customer(User):
    def __init__(self, name, email, address,account_type) -> None:
        super().__init__(name, email, address)
        self.balance = 0
        self.account_number = random.randint(1,500)
        self.account_type = account_type
        self.loan_limit = 0
        self.transaction_history = []


    def available_balance(self):
        print(f"Your Available Balance is : {self.balance}")


    def deposit(self,amount):
        if amount > 0:
            self.balance += amount
            save = Transaction_history("deposit",amount)
            self.transaction_history.append(save)
            print(f"**** {amount} tk deposited successfully ****")
        else:
            print("Your Amount is less than 0")



    def withdraw(self,bank,amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        elif amount < 0:
            print("Your Withdrawal amount is less than 0")
        elif bank.is_bankrupt == True:
            print("** the bank is bankrupt -->")
        else:
            self.balance -= amount
            save = Transaction_history("withdraw",amount)
            self.transaction_history.append(save)
            print(f"**** Withdraw {amount}  tk processed Successfully ****")



    def take_a_loan(self,bank,amount):
        
        if self.loan_limit <= 2:
            if amount < 0:
                print("your request amount is less than 0")
            elif amount > bank.total_balance:
                print("Your request amount is out of bound of bank total balance")
            elif bank.loan_status == False:
                print("You can't take loan from bank")
            else:
                self.balance += amount
                save = Transaction_history("loan",amount)
                self.transaction_history.append(save)
                self.loan_limit += 1
                bank.total_balance -= amount
                bank.total_loan += amount
                print("**** loan has been taken Successfully ****")
        else:
            print("Your Loan Limit Exceeded")


    def check_transaction_history(self):
        print("*****Transaction History*****")
        print("**** Details\tAmount ****")
        for transaction in self.transaction_history:
            print(f"**** {transaction.type} {transaction.amount}")


    def transfer_amount(self,bank,account_no,amount):
        search = bank.find_account(account_no)
        if search:
            if amount < 0:
                print("your request amount is less than 0")
            elif amount > self.balance:
                print("Your amount is out of your balance")
            elif bank.is_bankrupt == True:   
                print("the bank is bankrupt!!")
            else:
                print("search-->")
                print(search.balance)
                search.balance += amount
                self.balance -= amount
                save = Transaction_history("transfer money",amount)
                self.transaction_history.append(save)
                print(f"**** {amount} tk has been transferred successfully ****")
        else:
            print("Account does not exist!!")


class Transaction_history:
    def __init__(self,type,amount) -> None:
        self.type = type
        self.amount = amount


class Admin(User):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address)

    
Pubali_bank = Bank("Pubali Bank")
admin = Admin("admin","admin@gmail.com","Rajshahi")
Pubali_bank.create_admin(admin)

def user_menu():
    while True:
        currentUser = None

        print("1. Login\n2. Registration\n3. Exit")

        choice = int(input("Enter your option : "))

        if choice == 1:

            account_no = int(input("Enter your Account No : "))
            name = input("Enter your Name : ")
            match = False
            for users in Pubali_bank.account_list:
                if users.account_number == account_no and users.name == name.lower():
                    currentUser = users
                    match = True
                    break
            if match == False:
                print("<--No User Found-->")
            else:
                print("**** Login Successfully ****")


        elif choice == 2:

            name = input("Enter your Name : ")
            email = input("Enter your Email : ")
            address = input("Enter your Address : ")
            print("Account-type:")
            print("1.Savings\n2.Current")
            type = int(input("Choose: "))
            accountType = ""
            if type == 1:
                accountType = "Savings"
            elif type == 2:
                accountType = "Current"
            user = Customer(name,email,address,accountType)
            currentUser = user
            Pubali_bank.create_account(user)
            print(f"--> Registration Successfully -->(Your Account number is : {user.account_number})")


        if currentUser != None:

            while True:
                print(f"Welcome {currentUser.name}")
                print("1. Available Balance")
                print("2. Transaction History")
                print("3. Take a Loan")
                print("4. Deposit")
                print("5. Withdraw")
                print("6. Transfer Amount")
                print("7. Exit")


                choice = int(input("Enter Your Choice : "))


                if choice == 1:
                    user.available_balance()
                elif choice == 2:
                    user.check_transaction_history()
                elif choice == 3:
                    amount = int(input("Enter your request amount : "))
                    user.take_a_loan(Pubali_bank,amount)
                elif choice == 4:
                    amount = int(input("Enter your deposit amount : "))
                    user.deposit(amount)
                elif choice == 5:
                    amount = int(input("Enter your withdraw amount : "))
                    user.withdraw(Pubali_bank,amount)
                elif choice == 6:
                    account_no = int(input("Enter the user account number : "))
                    amount = int(input("Enter your amount : "))
                    user.transfer_amount(Pubali_bank,account_no,amount)
                elif choice == 7:
                    break
                else:
                    print("Invalid!!")

        elif choice == 3:
            break           


def admin_menu():
    while True:

        print("1. Login\n2. Exit")
        current_admin = None
        choice = int(input("Enter your option : "))

        if choice == 1:
            name = input("Enter your Name : ")
            email = input("Enter your Email : ")
            flag = False
            for adm in Pubali_bank.admin_list:
                if name == adm.name and email == adm.email:
                    current_admin = adm
                    flag = True
                    break
            if flag == False:
                print("**** User Not Found ****")
            else:
                print("**** Admin Login Successfully ****")

        elif choice == 2:
            break


        if current_admin != None:
            while True:
                print(f"** Welcome {admin.name} **")
                print("1. Delete User")
                print("2. See all User")
                print("3. Total Bank Balance")
                print("4. Total Bank Loan Balance")
                print("5. On or Off the loan feature")
                print("6. Exit")
                choice = int(input("Enter Your Choice : "))

                if choice == 1:
                    account = int(input("Enter the Account No : "))
                    Pubali_bank.delete_account(account)
                elif choice == 2:
                    Pubali_bank.show_users()
                elif choice == 3:
                    Pubali_bank.check_balance()
                elif choice == 4:
                    Pubali_bank.check_loan()
                elif choice == 5:
                    print(f"1.Turn on Loan\n2. Turn off loan")
                    select = int(input("Select your choice : "))
                    Pubali_bank.loan_feature(select) 
                elif choice == 6:
                    break
                else:
                    print("Invalid!!")


while True:
    print("Welcome!!")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        user_menu()
    elif choice == 2:
        admin_menu()
    elif choice == 3:
        break
    else:
        print("Invalid input!!")


