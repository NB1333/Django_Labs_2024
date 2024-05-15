import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User, Account, Transaction
from .storage import load_data, save_data
from django.shortcuts import render, redirect

# File path to the JSON storage
FILE_PATH = 'data/storage.json'

def get_data():
    try:
        return load_data(FILE_PATH)
    except FileNotFoundError:
        # Initial empty data structure if file doesn't exist
        return {'users': [], 'accounts': [], 'transactions': []}

def list_users(request):
    data = load_data('data/storage.json')
    return render(request, 'list_users.html', {'users': data['users']})

def list_accounts(request):
    accounts = load_data('data/storage.json')
    return render(request, 'list_accounts.html', {'accounts': accounts})

def list_transactions(request):
    transactions = load_data('data/storage.json')
    return render(request, 'list_transactions.html', {'transactions': transactions})

def write_data(data):
    save_data(FILE_PATH, data)


def create_user(request):
    if request.method == 'POST':
        user_data = {
            'id': request.POST['id'],
            'name': request.POST['name']
        }
        data = load_data('data/storage.json')
        data['users'].append(user_data)
        save_data('data/storage.json', data)
        return redirect('read_user', user_id=user_data['id'])
    return render(request, 'create_user.html')

# def read_user(request, user_id):
#     data = load_data('data/storage.json')
#     user = next((item for item in data['users'] if item['id'] == user_id), None)
#     transactions = [transaction for transaction in data['transactions'] if transaction['user_id'] == user_id]
#     if request.method == 'POST':
#         user['name'] = request.POST.get('name', user['name'])
#         save_data('data/storage.json', data)
#         return redirect('read_user', user_id=user_id)
#     if user:
#         return render(request, 'read_user.html', {'user': user, 'transactions': transactions})
#     return redirect('list_users')

def read_user(request, user_id):
    data = load_data('data/storage.json')
    user = next((item for item in data['users'] if item['id'] == user_id), None)
    transactions = [transaction for transaction in data['transactions'] if transaction['user_id'] == user_id]
    if request.method == 'POST':
        user['name'] = request.POST.get('name', user['name'])
        save_data('data/storage.json', data)
        return redirect('read_user', user_id=user_id)
    if user:
        # Check if the user has an account
        account = next((acc for acc in data['accounts'] if acc['user_id'] == user_id), None)
        context = {'user': user, 'account': account, 'transactions': transactions}
        return render(request, 'read_user.html', context)
    return redirect('list_users')

def delete_user(request, user_id):
    if request.method == 'POST':
        data = load_data('data/storage.json')
        data['users'] = [user for user in data['users'] if user['id'] != user_id]
        save_data('data/storage.json', data)
        return redirect('list_users')
    return redirect('read_user', user_id=user_id)

def transactions(request):
    data = load_data('data/storage.json')
    return render(request, 'list_transactions.html', {'transactions': data.get('transactions', [])})

def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        data = load_data('data/storage.json')
        data['transactions'] = [transaction for transaction in data['transactions'] if transaction['id'] != transaction_id]
        save_data('data/storage.json', data)
        return redirect(request.META.get('HTTP_REFERER', 'list_users'))  # Redirect back to the user's page
    return redirect('list_users')

def add_transaction(request):
    if request.method == 'POST':
        new_transaction = {
            'id': request.POST.get('id'),
            'user_id': request.POST.get('user_id'),
            'amount': request.POST.get('amount'),
        }
        data = load_data('data/storage.json')
        data['transactions'].append(new_transaction)
        save_data('data/storage.json', data)
        return redirect('transactions')
    return render(request, 'list_transactions.html')

def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        data = load_data('data/storage.json')
        data['transactions'] = [t for t in data['transactions'] if t['id'] != transaction_id]
        save_data('data/storage.json', data)
        return redirect('transactions')

def create_account(request, user_id):
    if request.method == 'POST':
        # Assuming form data is valid and POST contains necessary data
        data = load_data('data/storage.json')
        new_account = {
            'id': str(len(data['accounts']) + 1),  # Simple ID generation
            'user_id': user_id,
            'balance_uah': 0,
            'balance_usd': 0
        }
        data['accounts'].append(new_account)
        save_data('data/storage.json', data)
        return redirect('account_details', account_id=new_account['id'])
    # GET request shows a form to create the account
    return render(request, 'create_account.html', {'user_id': user_id})


def deposit_money(request, account_id):
    if request.method == 'POST':
        data = load_data('data/storage.json')
        account = next((acc for acc in data['accounts'] if acc['id'] == account_id), None)
        amount = float(request.POST.get('amount'))
        currency = request.POST.get('currency')  # 'uah' or 'usd'

        if currency == 'uah':
            account['balance_uah'] += amount
        elif currency == 'usd':
            account['balance_usd'] += amount
        
        save_data('data/storage.json', data)
        return redirect('account_details', account_id=account_id)
    return render(request, 'python_web_2024/deposit_money.html', {'account_id': account_id})


def exchange_money(request, account_id):
    if request.method == 'POST':
        data = load_data('data/storage.json')
        account = next((acc for acc in data['accounts'] if acc['id'] == account_id), None)
        amount = float(request.POST.get('amount'))
        direction = request.POST.get('direction')  # 'uah_to_usd' or 'usd_to_uah'

        if direction == 'uah_to_usd':
            if account['balance_uah'] < amount:
                return render(request, 'python_web_2024/error.html', {'message': 'Insufficient UAH balance'})
            exchanged_amount = amount / 40
            account['balance_uah'] -= amount
            account['balance_usd'] += exchanged_amount
        elif direction == 'usd_to_uah':
            if account['balance_usd'] < amount:
                return render(request, 'python_web_2024/error.html', {'message': 'Insufficient USD balance'})
            exchanged_amount = amount * 40

def account_details(request, account_id):
    data = load_data('data/storage.json')
    try:
        # Attempt to find the account
        account = next(acc for acc in data['accounts'] if acc['id'] == account_id)
    except StopIteration:
        # If no account is found, perhaps redirect back to a safe page or show an error
        return redirect('list_users')  # Redirect to the user list or an appropriate page

    return render(request, 'account_details.html', {'account': account})


# Users
# @require_http_methods(["POST"])
# def create_user(request):
#     data = get_data()
#     new_user = User(id=request.POST.get('id'), name=request.POST.get('name'))
#     data['users'].append(new_user.__dict__)
#     write_data(data)
#     return JsonResponse({'status': 'User created', 'user': new_user.__dict__})

# @require_http_methods(["GET"])
# def read_user(request, user_id):
#     data = get_data()
#     user = next((item for item in data['users'] if item['id'] == user_id), None)
#     if user:
#         return JsonResponse({'status': 'User found', 'user': user})
#     else:
#         return JsonResponse({'status': 'User not found'}, status=404)

# @require_http_methods(["POST"])
# def update_user(request, user_id):
#     data = get_data()
#     user = next((item for item in data['users'] if item['id'] == user_id), None)
#     if user:
#         user['name'] = request.POST.get('name', user['name'])
#         write_data(data)
#         return JsonResponse({'status': 'User updated', 'user': user})
#     else:
#         return JsonResponse({'status': 'User not found'}, status=404)

# @require_http_methods(["DELETE"])
# def delete_user(request, user_id):
#     data = get_data()
#     users = data['users']
#     user = next((item for item in users if item['id'] == user_id), None)
#     if user:
#         data['users'] = [user for user in users if user['id'] != user_id]
#         write_data(data)
#         return JsonResponse({'status': 'User deleted'})
#     else:
#         return JsonResponse({'status': 'User not found'}, status=404)

# Accounts
# @require_http_methods(["POST"])
# def create_account(request):
#     data = get_data()
#     new_account = Account(id=request.POST.get('id'), user_id=request.POST.get('user_id'), balance=float(request.POST.get('balance')))
#     data['accounts'].append(new_account.__dict__)
#     write_data(data)
#     return JsonResponse({'status': 'Account created', 'account': new_account.__dict__})

# @require_http_methods(["GET"])
# def read_account(request, account_id):
#     data = get_data()
#     account = next((item for item in data['accounts'] if item['id'] == account_id), None)
#     if account:
#         return JsonResponse({'status': 'Account found', 'account': account})
#     else:
#         return JsonResponse({'status': 'Account not found'}, status=404)

# @require_http_methods(["POST"])
# def update_account(request, account_id):
#     data = get_data()
#     account = next((item for item in data['accounts'] if item['id'] == account_id), None)
#     if account:
#         account['balance'] = float(request.POST.get('balance', account['balance']))
#         write_data(data)
#         return JsonResponse({'status': 'Account updated', 'account': account})
#     else:
#         return JsonResponse({'status': 'Account not found'}, status=404)

# @require_http_methods(["DELETE"])
# def delete_account(request, account_id):
#     data = get_data()
#     accounts = data['accounts']
#     account = next((item for item in accounts if item['id'] == account_id), None)
#     if account:
#         data['accounts'] = [account for account in accounts if account['id'] != account_id]
#         write_data(data)
#         return JsonResponse({'status': 'Account deleted'})
#     else:
#         return JsonResponse({'status': 'Account not found'}, status=404)

# # Transactions
# @require_http_methods(["POST"])
# def create_transaction(request):
#     data = get_data()
#     new_transaction = Transaction(
#         id=request.POST.get('id'), 
#         account_from=request.POST.get('account_from'), 
#         account_to=request.POST.get('account_to'), 
#         amount=float(request.POST.get('amount'))
#     )
#     data['transactions'].append(new_transaction.__dict__)
#     write_data(data)
#     return JsonResponse({'status': 'Transaction created', 'transaction': new_transaction.__dict__})

# @require_http_methods(["GET"])
# def read_transaction(request, transaction_id):
#     data = get_data()
#     transaction = next((item for item in data['transactions'] if item['id'] == transaction_id), None)
#     if transaction:
#         return JsonResponse({'status': 'Transaction found', 'transaction': transaction})
#     else:
#         return JsonResponse({'status': 'Transaction not found'}, status=404)

# @require_http_methods(["POST"])
# def update_transaction(request, transaction_id):
#     data = get_data()
#     transaction = next((item for item in data['transactions'] if item['id'] == transaction_id), None)
#     if transaction:
#         transaction['amount'] = float(request.POST.get('amount', transaction['amount']))
#         write_data(data)
#         return JsonResponse({'status': 'Transaction updated', 'transaction': transaction})
#     else:
#         return JsonResponse({'status': 'Transaction not found'}, status=404)

# @require_http_methods(["DELETE"])
# def delete_transaction(request, transaction_id):
#     data = get_data()
#     transactions = data['transactions']
#     transaction = next((item for item in transactions if item['id'] == transaction_id), None)
#     if transaction:
#         data['transactions'] = [trans for trans in transactions if trans['id'] != transaction_id]
#         write_data(data)
#         return JsonResponse({'status': 'Transaction deleted'})
#     else:
#         return JsonResponse({'status': 'Transaction not found'}, status=404)
