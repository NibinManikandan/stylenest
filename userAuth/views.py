from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
import random
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin




# Create your views here.

# user login page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def user_Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)

            if user is not None:
                custom_user = CustomUser.objects.filter(email=email).first()

                if custom_user is not None and not custom_user.is_active:
                    messages.error(request, 'Your Access Denied')
                else:
                    login(request, user)
                    request.session['user'] = email
                    return redirect('home')
            else:
                # User does not exist or invalid email/password
                messages.error(request, 'User does not exist or invalid email/password')
        else:
            messages.error(request, 'Email and password are required')

    return render(request, 'User_/user_login.html')



# sending otp for varification into mail
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def send_otp_email(request):
    email=request.session.get('email')
    otp = random.randint(100000, 999999)
    print(otp)




# sending otp
    
    subject = 'Email Verification OTP'
    message = f'''Hello Customer,

Thank you for signing up with StyleNest! Your OTP (One-Time Password) for account verification is: {otp}.

Please enter this OTP on the Stylenest website to complete your account verification process.

Thanks,
The StyleNest Team'''

    request.session['otp'] = otp

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)

    return redirect('otp_page')



# creating user
def user_Signup(request):
    if request.method == "POST":
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        paswrd = request.POST.get('password')
        confirm_password = request.POST.get('cnf_pass')

        # Check if first name contains only alphabets and no spaces
        if not f_name.isalpha():
            return redirect('signup')

        # Check if last name contains only alphabets and no spaces
        if not l_name.isalpha():
            return redirect('signup')

        # Check if phone number is valid (e.g., contains only digits and has a length of 10)
        if not phone.isdigit() or len(phone) != 10:
            return redirect('signup')

        # Check if email is already registered
        if CustomUser.objects.filter(email=email).exists():
            return redirect('signup')
        
        if CustomUser.objects.filter(phone=phone).exists():
            return redirect('signup')
        

        # Check if passwords match
        if paswrd != confirm_password:
            return redirect('signup')
        
        request.session['email']=email
        send_otp_email(request)

        # All validations passed, create the user
        user = CustomUser.objects.create_user(
            username=email,
            first_name=f_name,
            last_name=l_name,
            phone=phone,
            email=email,
            password=paswrd
        )

        request.session['current'] = user.id

        # Redirect to OTP verification page 
        return redirect('otp_page')

    else:
        return render(request, 'User_/user_signup.html')




# otp varifying
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = {
        'otp1': request.POST.get('otp1'),
        'otp2': request.POST.get('otp2'),
        'otp3': request.POST.get('otp3'),
        'otp4': request.POST.get('otp4'),
        'otp5': request.POST.get('otp5'),
        'otp6': request.POST.get('otp6'),
        }

        # Concatenate values as strings
        otp_values = ''.join(str(value) for value in entered_otp.values() if value is not None)
        # Convert concatenated string to integer
        otp_int = str(otp_values)

        user_id = request.session['current']
        user = CustomUser.objects.get(id=user_id)
        
        # Checking the entered OTP matches to actual OTP
        if otp_int == str(request.session['otp']):
            user.is_active = True
            user.save() 
            messages.success(request, 'OTP verified successfully!')
            return render(request, 'User_/user_login.html')
        
        else:    
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp_page')
    else:      
        return render(request, 'User_/otp_page.html')        
    


# user logout section
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache    
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('Userlogin')

