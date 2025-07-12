from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomUser, Jobs, Proposals
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
        return redirect('jobs')

    return render(request, 'signup.html',{'customuser': customuser})
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('jobs')            
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def freelancer(request):
    proposal_count = Proposals.objects.filter(freelancer=request.user.customuser).count()
    return render(request, 'freelancer.html',{'proposal_count':proposal_count})
def client(request):
    return render(request, 'client.html')
def jobs(request):
    jobs = Jobs.objects.all()
    applied_job_ids = []
    if request.user.is_authenticated and request.user.customuser.account_type == 'freelancer':
        freelancer = request.user.customuser
        applied_job_ids = Proposals.objects.filter(freelancer=freelancer).values_list('job_id', flat=True)

    return render(request, 'jobs.html',{'jobs': jobs,'applied_job_ids': applied_job_ids})

def logout_user(request):
    logout(request)
    return redirect('home')

def postjob(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        deadline = request.POST.get('deadline')
        status = request.POST.get('status')

        # Save the job to the database
        job = Jobs(client=request.user.customuser, title=title, description=description, budget=budget, deadline=deadline, status=status)
        job.save()

        return redirect('jobs')
    return render(request, 'postjob.html')

def apply(request, job_id):
    freelancer = request.user.customuser
    job = Jobs.objects.get(id=job_id)
    if request.method == 'POST':
       message = request.POST.get('proposal')
       budget = request.POST.get('budget')
       duration = request.POST.get('duration')
       portfolio_url = request.POST.get('portfolio_url')
       attachment = request.FILES.get('attachment')

       # Save the proposal to the database  
       proposal = Proposals(freelancer=freelancer, job=job, proposal=message, budget=budget, duration=duration, portfolio_url=portfolio_url, attachment=attachment)
       proposal.save()
       messages.success(request, 'Proposal submitted successfully!')
       return redirect('jobs')
    return render(request, 'apply.html',{'job':job})

def client_proposals(request):
    if  not request.user.is_authenticated:
        messages.warning(request,'Login required')
        return redirect('login')
    customuser = request.user.customuser
    
    if customuser.account_type != 'client':
        return redirect('home') 
    
    client_jobs = Jobs.objects.filter(client=customuser)
    proposals = Proposals.objects.filter(job__in=client_jobs)
    return render(request, 'client_proposals.html',{'proposals':proposals})

