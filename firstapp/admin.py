from django.contrib import admin
from .models import Client, Category, Employee, Ticket

admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Ticket)
