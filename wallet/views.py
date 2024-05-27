from http import client
from django.shortcuts import render, redirect
from userAuth.models import *
from .models import *
import razorpay
from dotenv import load_dotenv
import os
from django.views.decorators.csrf import csrf_exempt
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




load_dotenv()

RAZORPAY_KEY_ID = os.getenv('rzp_test_F4i5wCsFw7GaJK')
RAZORPAY_KEY_SECRET = os.getenv('QHYtPSDOho5w5YCvh5ZFvRFo')

client = razorpay.Client(auth=("rzp_test_F4i5wCsFw7GaJK", "QHYtPSDOho5w5YCvh5ZFvRFo"))

# function for add amount to wallet
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_amount(request):
    amount = request.POST.get('amount')
    if not amount:
        return JsonResponse({"success": False, "message": "Amount is required."})

    try:
        amount = int(amount)
        if amount < 1:
            return JsonResponse({"success": False, "message": "Amount must be at least 1 INR."})
        amount_in_paise = amount * 100
    except ValueError:
        return JsonResponse({"success": False, "message": "Invalid amount format."})

    data = {'amount': amount_in_paise, 'currency': 'INR'}
    payment = client.order.create(data=data)
    request.session['amount'] = amount

    return JsonResponse({
        "success": True,
        "payment": payment,
        "payment_id": payment['id'],
        "amount": amount_in_paise
    })




@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_wallet(request):
    if request.user:
        email = request.user
        amount = request.session["amount"]
        user_name = CustomUser.objects.get(email=email)
        user = Wallet.objects.filter(user=user_name).order_by("-id").first()
        balance = user.balance if user else 0

        new_balance = balance + amount
        Wallet.objects.create(
            user=user_name,
            amount=amount,
            balance=new_balance,
            transaction_type="Credit",
            transaction_details=f"Added Money through Razorpay",
        )

        return redirect("wallet")
    else:
        return JsonResponse({'success':False,'message': 'User not logged in'}, status=400)