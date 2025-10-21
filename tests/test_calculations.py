from app.calculations import BankAccount, add
import pytest


@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.fixture
def zero_bank_account():
    return BankAccount()




@pytest.mark.parametrize("num1, num2, expected",[(2,3,5), (7,1,8), (4,16,20)])
def test_add(num1, num2, expected):
    sum = add(num1, num2)
    
    assert sum == expected
    
def test_bank_initial_amount(bank_account):
    # bank_account = BankAccount(30)
    
    assert bank_account.balance == 50
    
    
def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    
    assert zero_bank_account.balance == 0
    
def test_bank_deposite(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70
    
    
def test_bank_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    