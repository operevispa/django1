from django.urls import path
from .views import index, create_client, create_employee, create_ticket, tickets


urlpatterns = [
    path('', index),
    path('create_client/', create_client),
    path('create_employee/', create_employee),
    path('create_ticket/', create_ticket),
    path('tickets/', tickets),
]
