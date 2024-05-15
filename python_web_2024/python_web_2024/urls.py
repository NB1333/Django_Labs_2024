"""
URL configuration for python_web_2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # User URLs
    path('users/', views.list_users, name='list_users'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/<str:user_id>/', views.read_user, name='read_user'),
    path('user/update/<str:user_id>/', views.read_user, name='read_user'),
    path('user/delete/<str:user_id>/', views.delete_user, name='delete_user'),
    path('transaction/delete/<str:transaction_id>/', views.delete_transaction, name='delete_transaction'),

    # Account URLs
    path('account/<str:account_id>/', views.account_details, name='account_details'),
    path('account/create/<str:user_id>/', views.create_account, name='create_account'),
    path('account/deposit/<str:account_id>/', views.deposit_money, name='deposit_money'),
    path('account/exchange/<str:account_id>/', views.exchange_money, name='exchange_money'),

    # Transaction URLs
    path('transactions/', views.transactions, name='list_transactions'),
    path('transaction/create/', views.add_transaction, name='add_transaction'),
    # path('transaction/<str:transaction_id>/', views.read_transaction, name='read_transaction'),
    path('transaction/update/<str:transaction_id>/', views.add_transaction, name='update_transaction'),
    path('transaction/delete/<str:transaction_id>/', views.delete_transaction, name='delete_transaction'),

]
