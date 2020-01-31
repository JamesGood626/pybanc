from flask import Flask, request, render_template, make_response, jsonify
from account.index import *
app = Flask(__name__)


def create_cookie_resp(fn, acc_num):
    resp = make_response(fn())
    resp.set_cookie('acc_num', acc_num)
    return resp


@app.route('/view-state')
def view_state():
    return jsonify(view_accounts_state())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
        If request is POST,
            we look generate an account number for the new user
            then create a cookie so that their acc_num is accessible
            in subsequent requests, and redirect them to account.html.
        If request is GET
            we just render signup.html
    """
    if request.method == 'POST':
        acc_num, balance = generate_account_number()
        # resp = make_response(render_template(
        #     'account.html', acc_num=acc_num, balance=balance))
        # resp.set_cookie('acc_num', acc_num)
        # return resp
        return create_cookie_resp(lambda: render_template(
            'account.html', acc_num=acc_num, balance=balance), acc_num)
    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """
        If request is POST,
            we look up the user's account by the acc_num they submitted in the form.
            If they have an account present, then we redirect them to the account page.
            Else if the acc_num is submitted is invalid, then we show an error.
        If request is GET
            we just render signin.html
    """
    if request.method == 'POST':
        acc_num = request.form["acc_num"]
        result = retrieve_account(acc_num)
        if result == "ACCOUNT_DOES_NOT_EXIST":
            return render_template('signin.html', error="That account does not exist.")
        else:
            return create_cookie_resp(lambda: render_template(
                'account.html', acc_num=acc_num, balance=result), acc_num)
    return render_template('signin.html')


@app.route('/deposit', methods=['POST'])
def deposit():
    acc_num = request.cookies.get('acc_num')
    amount = request.form['amount']
    new_balance = make_deposit(acc_num, amount)
    return render_template('account.html', acc_num=acc_num, balance=new_balance)


@app.route('/withdraw', methods=['POST'])
def withdraw():
    acc_num = request.cookies.get('acc_num')
    amount = request.form['amount']
    new_balance = make_withdraw(acc_num, amount)
    if new_balance == "INSUFFICIENT_FUNDS":
        return render_template('account.html', acc_num=acc_num, balance=get_balance(acc_num), withdraw_error="You don't have sufficient funds to withdraw from.")
    return render_template('account.html', acc_num=acc_num, balance=new_balance)


@app.route('/transfer', methods=['POST'])
def transfer():
    acc_num = request.cookies.get('acc_num')
    target_account = request.form['target_account']
    amount = request.form['amount']
    new_balance = make_transfer(acc_num, target_account, amount)
    if new_balance == "INSUFFICIENT_FUNDS":
        return render_template('account.html', acc_num=acc_num, balance=get_balance(acc_num), transfer_error="You don't have sufficient funds to complete the transfer.")
    return render_template('account.html', acc_num=acc_num, balance=new_balance)
