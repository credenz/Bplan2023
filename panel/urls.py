from django.urls import path
from .views import * 
urlpatterns = [
    path('panel/<str:company_id>/',dashboard,name='dashboard'),
    path('instructions/',instructions,name='instructions'),
    path('create_team/',create_team,name="create_team"),
    path('result/',result,name="result")
]
