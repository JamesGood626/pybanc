from random import seed, random

seed(20)

accounts = {}


def view_accounts_state():
    return accounts


def generate_account_number():
    """
        value assigned to acc_num is a float converted to a string,
        so the first two characters are sliced.

        Then if the acc_num already exists in accounts, we recursively call,
        generate_account_number until a unique acc_num is generated.
    """
    acc_num = str(random())[2:]
    if acc_num in accounts:
        generate_account_number()
    accounts[acc_num] = {
        'balance': 0
    }
    return acc_num, accounts[acc_num]['balance']


def retrieve_account(acc_num):
    if acc_num in accounts:
        return accounts[acc_num]['balance']
    else:
        return "ACCOUNT_DOES_NOT_EXIST"


def get_balance(acc_num):
    return accounts[acc_num]['balance']


def make_deposit(acc_num, amount):
    old_balance = accounts[acc_num]['balance']
    new_balance = old_balance + int(amount)
    accounts[acc_num]['balance'] = new_balance
    return new_balance


def make_withdraw(acc_num, amount):
    old_balance = accounts[acc_num]['balance']
    if old_balance < int(amount):
        return "INSUFFICIENT_FUNDS"
    new_balance = old_balance - int(amount)
    accounts[acc_num]['balance'] = new_balance
    return new_balance


def make_transfer(acc_num, target_account, amount):
    if target_account in accounts:
        new_balance = make_withdraw(acc_num, amount)
        if new_balance == 'INSUFFICIENT_FUNDS':
            return new_balance
        accounts[target_account]['balance'] = accounts[target_account]['balance'] + \
            int(amount)
        return new_balance
