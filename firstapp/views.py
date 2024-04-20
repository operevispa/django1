from django.shortcuts import render
from .forms import NewEmployeeForm, NewClientForm, CreateTicketForm
from .demo import *


# стартовая страница с информацией о проекте и ссылками на основные функции
def index(request):
    return render(request, "index.html")


# функция создания нового клиента в БД
def create_client(request):

    if request.method == "POST":
        newclient = Client()
        newclient.phone = request.POST.get("phone")
        newclient.email = request.POST.get("email")
        newclient.fname = request.POST.get("fname")
        newclient.lname = request.POST.get("lname")
        newclient.save()

        return render(request, "success.html", {"item": "клиент"})
    else:
        newclientform = NewClientForm()
        return render(request, "newuser.html",
                      {"item": "клиент", "form": newclientform})


# внесение информации о новом сотруднике в базу данных
def create_employee(request):
    newempform = NewEmployeeForm(request.POST or None)

    # проверяем валидность введенных пользователем данных в форму
    if newempform.is_valid():
        # пользователь ввел корректные данные, значит создаем объект класса Employee
        newemployee = Employee()

        # вносим данные из форм заполненных пользователем в поля объекта класса, для последующей записи в БД
        newemployee.fname = request.POST.get("fname")
        newemployee.lname = request.POST.get("lname")
        newemployee.phone = request.POST.get("phone")
        newemployee.email = request.POST.get("email")

        try:
            # пытаемся найти категорию в БД
            newemployee.category = Category.objects.get(id=request.POST.get("category"))
        except Category.DoesNotExist:
            # если категорию в БД не находим, то записываем категорию по-умолчанию
            newemployee.category = Category.objects.get(id=0)
            # и выводим сообщение об ошибке в веб-форму
            data = {"form": newempform,
                    "errormes": "Категория " + request.POST.get("category") + " не найдена в базе данных!"}
            return render(request, "create_ticket.html", context=data)

        # если дошли до этого момента, значит с данными все впорядке, поля заполненны, сохраняем запись в БД
        newemployee.save()

        # перекидываем пользователя на страничку "успеха"
        return render(request, "success.html", {"item": "сотрудник"})
    else:
        # пользователь ввел невалидные данные, либо получен запрос GET
        # т.е. пользователь зашел первый раз на страницу и никакие данные еще не отправлял,
        # иначе сработал бы метод POST
        return render(request, "newuser.html",
                      {"item": "сотрудник", "form": newempform})


# создание новой задачи (тикета)
def create_ticket(request):
    # передаем в форму данные полученные из метода POST и файлы.
    # это на тот случай, если пользовтаель уже ввел какие-то данные, но они оказались невалидными
    # и чтобы заново все не вносить, мы возвращаем в форму ранее заполненные пользователем данные
    form = CreateTicketForm(request.POST or None, request.FILES or None)

    # проверяем валидность введенных в форму данных
    # (при первом запуске функции данные не валидны, поскольку их еще нет)
    if form.is_valid():

        # пользователь ввел валидные данные в поля формы - создаем экземпляр класса Ticket и записываем его в БД
        newticket = Ticket()
        newticket.tdate = datetime.now()
        newticket.audio_ticket = form.cleaned_data['audio_ticket']
        newticket.text_ticket = request.POST.get("text_ticket")
        newticket.priority = int(request.POST.get("priority"))

        # по email клиента пытаемся найти его в БД и в заявке указываем объект Клиент
        try:
            cl = Client.objects.get(phone=request.POST.get("phone"))
            newticket.client = cl
        except Client.DoesNotExist:
            # если клиент по номеру телефона не нашелся, выводим сообщение об ошибке в консоль и на веб-форму
            print("Клиент в базе не найден. Проверьте корректность введенного номера телефона")
            data = {"form": form,
                    "errormes": "Клиент в базе не найден. Проверьте корректность введенного номера телефона!"}
            return render(request, "create_ticket.html", context=data)

        # пытаемся найти категорию в смежной таблице БД
        try:
            newticket.category = Category.objects.get(id=int(request.POST.get("category")))
        except Category.DoesNotExist:
            # если категорию не находим, то указываем категорию по-умолчанию
            newticket.category = Category.objects.get(id=0)
            data = {"form": form,
                    "errormes": "Категория " + request.POST.get("category") + " не найдена в базе данных!"}
            return render(request, "create_ticket.html", context=data)

        # пытаемся найти сотрудника в БД по введенным пользователем данным
        try:
            newticket.employee = Employee.objects.get(id=int(request.POST.get("employee")))
        except Employee.DoesNotExist:
            # если сотрудника не находим, то указываем неопределенного сотрудника (специально создан для этого в БД)
            newticket.employee = Employee.objects.get(id=0)
            data = {"form": form,
                    "errormes": "Сотрудник с кодом " + request.POST.get("employee") + " не найден в базе данных"}
            return render(request, "create_ticket.html", context=data)

        # сохраняем объект (новую заявку) в базе данных
        newticket.save()
        return render(request, "success.html", {"item": "тикет"})

    else:
        # пользователь ввел невалидные данные в форму, либо произошел первый запуск формы
        print(form.errors)
        return render(request, "create_ticket.html", context={"form": form})


# отображение списка всех тикетов (заданий)
def tickets(request):
    return render(request, "tickets.html", context={"tikets": Ticket.objects.all()})


create_demo_category()
create_demo_clients()
create_demo_employee()
create_demo_ticket()
