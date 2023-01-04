'''
-create a set of test cases to test a bank Account class. 
-Each new Account must have:
	-an account number
	-a date of opening
	-an interest rate
	-an opening balance. 
-It must support methods to:
	-deposit money
	-withdraw money
	-transfer money between accounts. 
-Do not implement the Account class (a dummy implementation is enough - all methods should just "pass") and hence all tests shall fail. 
'''
import unittest
import datetime

class BankAccount():
    def __init__(self, account_num: str, opened_at: datetime.date, 
                interest_rate: float, balance: float) -> None:
        self.account_num = account_num
        self.opened_at = opened_at
        self.interest_rate = interest_rate
        self.balance = balance

    def deposit(self, amount):
        pass
    
    def withdraw(self, amount):
        pass

    def transfer(self, amount, to_account):
        #if self.balance >= amount:
        #    to_account.balance += amount
        #    self.balance -= amount
        pass


class AccountTestCase(unittest.TestCase): 

    def test_deposit(self):
        acc = BankAccount('wsr5uj', '04-01-2023', 2.5, 200) 
        acc.deposit(150)
        self.assertEqual(acc.balance, 350) 


    def test_withdraw(self): 
        acc = BankAccount('wsr5uj', '04-01-2023', 2.5, 200) 
        acc.withdraw(150)
        self.assertEqual(acc.balance, 50) 


    def test_transfer(self): 
        acc1 = BankAccount('wsr5uj', '04-01-2023', 2.5, 200)
        acc2 = BankAccount('9876jt', '04-01-2023', 3, 450) 
        acc2.transfer(450, acc1)
        self.assertEqual(acc2.balance, 0)