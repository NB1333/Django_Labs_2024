from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('users/', views.list_users, name='list_users'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/<str:user_id>/', views.read_user, name='read_user'),
    path('user/update/<str:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<str:user_id>/', views.delete_user, name='delete_user'),

    # Account URLs
    path('accounts/', views.list_accounts, name='list_accounts'),
    path('account/create/', views.create_account, name='create_account'),
    path('account/<str:account_id>/', views.read_account, name='read_account'),
    path('account/update/<str:account_id>/', views.update_account, name='update_account'),
    path('account/delete/<str:account_id>/', views.delete_account, name='delete_account'),

    # Transaction URLs
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('transaction/create/', views.add_transaction, name='create_transaction'),
    path('transaction/<str:transaction_id>/', views.read_transaction, name='read_transaction'),
    path('transaction/update/<str:transaction_id>/', views.update_transaction, name='update_transaction'),
    path('transaction/delete/<str:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]
