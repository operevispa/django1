from django.db import models


# модель для хранения данных по клиенту в базе данных
class Client(models.Model):
    phone = models.CharField(max_length=16, unique=True, blank=False)
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=20, blank=False)
    lname = models.CharField(max_length=20)

    def __str__(self):
        return self.fname + " " + self.lname


# модель для хранения категорий задач в базе данных
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + " " + self.category_name


# модель для хранения информации о сотрудниках компании
class Employee(models.Model):
    phone = models.CharField(max_length=16, unique=True, blank=False)
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=20, blank=False)
    lname = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.fname + " " + self.lname


# модель для хранения информации об инцидентах и задачах для сотрудников поддержки
class Ticket(models.Model):
    tdate = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    audio_ticket = models.FileField(upload_to="media")
    text_ticket = models.CharField(max_length=5000)
    priority = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Клиент: " + str(self.client) + ",    Категория задачи: " + str(
            self.category) + ",    Приоритет: " + str(self.priority)
