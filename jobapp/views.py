from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login as auth_login, authenticate,logout

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    customuser = None
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        account_type = request.POST.get('account_type')
        profilepicture = request.FILES.get('profilepicture')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        bio = request.POST.get('bio')
        companyname = request.POST.get('companyname')
        companysize = request.POST.get('companysize')
        companywebsite = request.POST.get('companywebsite')

        if password != confirmpassword:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')
        
        if account_type == 'client':
            if not companyname or not companysize:
                messages.error(request, 'Company details are required for clients')
                return render(request, 'signup.html')
        
        if account_type == 'freelancer':
            if not skills or not experience or not bio:
                messages.error(request, 'Skills and experience are required for freelancers')
                return render(request, 'signup.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        customuser = CustomUser.objects.create(
            user=user,
            fullname=fullname,
            account_type=account_type,
            profile_pic=profilepicture,
            skills=skills,
            experience=experience if experience else 0,
            bio=bio,
            company_name=companyname,
            company_size=companysize,
            company_website=companywebsite
        )
        
        auth_login(request, user)

        messages.success(request, 'Account created successfully')
        return redirect('jobs')

    return render(request, 'signup.html',{'customuser': customuser})
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('jobs')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def jobs(request):
    return render(request, 'jobs.html')