from http import client
from django.shortcuts import render, redirect
from userAuth.models import *
from .models import *
from django.http import JsonResponse
from django.views.decorators.cache import cache_control

# Create your views here.


# function for view wallet details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wallet(request):
    user = request.session["user"]
    user_name=CustomUser.objects.get(email = user)
    wallett = Wallet.objects.filter(user = user_name).order_by('-id')

    if wallett.exists():
        latest_transaction = wallett.first() 
        balance = latest_transaction.balance
    else:
        balance = 0  

    return render(request, 'platform/wallet.html', {'wallett':wallett, 'balance':balance})




# function for add amount to wallet
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_amount(request):
    print('wallet amount add')
    amount = int(request.POST.get('amount')) * 100
    data = {'amount':amount, 'currency':'INR'}
    payment = client.order.create(data=data)
    request.session['amount'] = amount / 100
    print(amount)

    return JsonResponse(
        {
            "success":True,
            "payment":payment,
            "payment_id":payment['id'],
            "amount":amount
        }
    )
