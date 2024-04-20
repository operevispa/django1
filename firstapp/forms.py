from django import forms
from .models import Employee, Category


# форма внесения данных по новому сотруднику
class NewEmployeeForm(forms.Form):
    fname = forms.CharField(label="Имя", max_length=20, required=True)
    lname = forms.CharField(label="Фамилия", max_length=20, required=False)
    phone = forms.CharField(label="Телефон", max_length=16, required=True)
    email = forms.EmailField(label="email", max_length=30, required=True)
    catlist = [(num, cat.category_name) for num, cat 
               in Category.objects.in_bulk().items()]
    category = forms.ChoiceField(label="Категория", choices=catlist)


# форма внесения данных нового клиента
class NewClientForm(forms.Form):
    fname = forms.CharField(label="Имя", max_length=20, required=True)
    lname = forms.CharField(label="Фамилия", max_length=20, required=False)
    phone = forms.CharField(label="Телефон", max_length=16, required=True)
    email = forms.EmailField(label="email", max_length=30, required=True)


# форма внесения данных по заявке (тикету)
class CreateTicketForm(forms.Form):
    phone = forms.CharField(label="Телефон", max_length=16, required=True)
    text_ticket = forms.CharField(label="Текст обращения", 
                                  max_length=5000, required=False, widget=forms.Textarea)
    priority = forms.ChoiceField(label="Приоритет", 
                                 choices=[(1, "высокий"), (2, "средний"), (3, "низкий")])
    catlist = [(num, cat.category_name) for num, cat 
               in Category.objects.in_bulk().items()]
    category = forms.ChoiceField(label="Категория", choices=catlist)
    emplist = [(num, emp.fname+" "+emp.lname) for num, emp 
               in Employee.objects.in_bulk().items()]
    employee = forms.ChoiceField(label="Сотрудник", choices=emplist)
    audio_ticket = forms.FileField(label="Файл аудиозаписи", widget=forms.FileInput)
