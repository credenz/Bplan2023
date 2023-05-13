from django.db import models
from django.contrib.auth.models import auth, User
from django.db.models import Sum

TOTAL_BUDGET = 100 

# Create your models here.
class Team(models.Model):
    Name = models.CharField(max_length=100)
    Leader = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    remaining_budget = models.FloatField(default=TOTAL_BUDGET, null=True)
    total_companies_bought = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.Name
    
class Domain(models.Model):
    name = models.CharField(max_length=10);

    def __str__(self) -> str:
        return self.name
    
class Company(models.Model):
    name = models.CharField(max_length=100, default="")
    base_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    domain = models.ForeignKey(Domain,on_delete=models.SET_NULL,null=True)
    team = models.ForeignKey(Team, on_delete = models.PROTECT, null = True, blank = True, related_name="companies")
    img = models.URLField(blank=True,null=True)

    def __str__(self) -> str:
        if(self.team):
            return self.name + " - " + self.team.Name
        else:
            return self.name
