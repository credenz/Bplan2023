from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.http import JsonResponse
from .models import Team,Company

# Create your views here.
def instructions(request):
    return render(request,'instructions.html')

def dashboard(request,company_id):
    if request.method == 'POST':
        company = Company.objects.get(id=company_id)
        team = Team.objects.get(id=request.POST['team'])
        if team.remaining_budget < float(request.POST['selling_price']):
            messages.error(request,"Team "+team.Name+"'s budget is low")
            return redirect(dashboard(company_id))
        company.selling_price = float(request.POST['selling_price'])
        company.team = team 
        company.save() 

        team.total_companies_bought += 1
        team.remaining_budget -= float(request.POST['selling_price'])
        team.save() 

        company_id=int(company_id)+1

    teams = Team.objects.all().order_by('-total_companies_bought')
    companies = Company.objects.all()

    if company_id != '0':
        if Company.objects.filter(id=company_id).exists():
            company = Company.objects.get(id=company_id)
        else:
            company = -1
    else:
        company = 0

    context = {
        'teams':teams,
        'companies':companies.order_by('domain'),
        'company':company,
    }
    return render(request,'dashboard.html',context)

def create_team(request):
    if request.method == 'POST':

        try:
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            user_name = request.POST['username']
            password = request.POST['password']
            user = User.objects.create(first_name=first_name,last_name=last_name,username=user_name,password=password)
            user.save()

            team_name = request.POST['teamname']
            team = Team.objects.create(Name=team_name,Leader=user)
            team.save()
            status = 'Ok'
        except Exception as e:
            status = str(e)

        return JsonResponse({'status':status})
    
def result(request):
    teams = Team.objects.all().order_by('remaining_budget')
    companies = Company.objects.all().order_by('domain')
    rating_dict = dict()
    for i in teams:
        rating_sum = 0
        for j in companies:
            if j.team == i:
                rating_sum+=j.rating
        rating_dict[i] = rating_sum / i.total_companies_bought
    context = {
        'teams':teams,
        'companies':companies,
        'rating_dict':rating_dict
    }
    return render(request,'result.html',context)