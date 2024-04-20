from .models import Client, Category, Employee, Ticket
from datetime import datetime


# функция созданяи демо-данных для проекта
def create_demo_category():
    # проверяем, заполнены ли в БД категории
    if not Category.objects.exists():
        # категорий в базе не оказалось, значит создаем их
        category = {0: "Не определено", 1: "Windows", 2: "Linux", 
                    3: "Сеть", 4: "Техника", 5: "Office, Open office"}
        
        # проходимся по каждому из элементов словаря
        for catid, catname in category.items():
            # создаем объект класса Category и сохраняем его сразу в БД
            cat = Category(id=catid, category_name=catname)
            cat.save()

        return print("Демо данные в таблице Category созданы!")


def create_demo_clients():
    # проверяем, заполнены ли в БД клиенты
    if not Client.objects.exists():

        clients = [{"phone": "+7 584 224-44-69", "email": 
                    "semenova@mail.ru", "fname": "Мария", "lname": "Семенова"},
                   {"phone": "+7 993 445-45-60", "email": "kozlova@mail.ru", 
                    "fname": "Елена", "lname": "Козлова"},
                   {"phone": "+7 985 444-78-99", "email": "koneva@gmail.com", 
                    "fname": "Василиса", "lname": "Конева"},
                   {"phone": "+7 985 004 81-54", "email": "pronin@mail.ru", 
                    "fname": "Анатолий", "lname": "Пронин"},
                   {"phone": "+7 008 484-77-77", "email": "stepanova@yahoo.com", 
                    "fname": "Анна", "lname": "Степанова"}
                   ]

        # создаем дефолтного клиента (будет указываться по умолчанию)
        client = Client(id=0, phone="None", email="None", fname="None", lname="None")
        client.save()

        i = 1
        # проходимся по каждому из элементов словаря
        for cl in clients:
            # создаем объект класса Client и сохраняем его сразу в БД
            client = Client(id=i, phone=cl["phone"], email=cl["email"], 
                            fname=cl["fname"], lname=cl["lname"])
            i += 1
            client.save()

        return print("Демо данные в таблице Client созданы!")


def create_demo_employee():
    # проверяем, заполнены ли в БД сотрудники
    if not Employee.objects.exists():

        employee = [{"phone": "+7 985 445-56-98", "email": "petrov@mail.ru", 
                     "fname": "Александр", "lname": "Петров",
                     "category": 1},
                    {"phone": "+7 844 138-48-74", "email": "boshirov@mail.ru", 
                     "fname": "Руслан", "lname": "Боширов",
                     "category": 5},
                    {"phone": "+7-456-987-45-24", "email": "mishkin@gmail.com", 
                     "fname": "Александр", "lname": "Мишкин",
                     "category": 2},
                    {"phone": "+7(456)445 44 56", "email": "chepiga@mail.ru", 
                     "fname": "Анатолий", "lname": "Чепига",
                     "category": 4},
                    {"phone": "+7-999-901-44-45", "email": "a.chapman@yahoo.com", 
                     "fname": "Анна", "lname": "Чапман",
                     "category": 3}
                    ]

        # создаем дефолтного сотрудника (будет указываться, когда реальный сотрудник не известен, или уволился)
        empl = Employee(id=0, phone="None", email="None", fname="None", lname="None",
                        category=Category.objects.get(id=0))
        empl.save()

        i = 1
        # проходимся по каждому из элементов словаря
        for em in employee:
            # создаем объект класса Employee и сохраняем его сразу в БД
            empl = Employee(id=i, phone=em["phone"], email=em["email"], 
                            fname=em["fname"], lname=em["lname"])

            try:
                empl.category = Category.objects.get(id=em["category"])
            except Category.DoesNotExist:
                empl.category = Category.objects.get(id=0)
                print("Категория с кодом", em["category"], "не найдена в базе данных")

            i += 1
            empl.save()

        return print("Демо данные в таблице Employee созданы!")


def create_demo_ticket():
    # проверяем, заполнены ли в БД заявки
    if not Ticket.objects.exists():

        tickets = [{"text_ticket": "Добрый день. У меня сломалась клавиатура. Ничего не могу напечатать,"
                                   "а завтра сдавать годовой отчет. Срочно нужна замена. Памагите!!",
                    "priority": 2, "category": 1, "client": 1, "employee": 3},
                   {"text_ticket": "Периодически включается порнуха. "
                                    "Спасите, это все вирусы. Я тут не причем.",
                    "priority": 3, "category": 2, "client": 2, "employee": 2},
                   {"text_ticket": "Винда глючит и тупит.",
                    "priority": 1, "category": 3, "client": 4, "employee": 1},
                   {"text_ticket": "Сломалась мышка. Прошу заменить",
                    "priority": 3, "category": 4, "client": 3, "employee": 4},
                   ]

        dt = 1
        # проходимся по каждому из элементов словаря
        for tic in tickets:
            # создаем объект класса Ticket и сохраняем его сразу в БД

            ticket = Ticket(tdate=datetime(2024, 2, dt), audio_ticket="", 
                            text_ticket=tic["text_ticket"], priority=tic["priority"])

            try:
                ticket.category = Category.objects.get(id=tic["category"])
            except Category.DoesNotExist:
                ticket.category = Category.objects.get(id=0)
                print("Категория с кодом", tic["category"], "не найдена в базе данных")

            try:
                ticket.employee = Employee.objects.get(id=tic["employee"])
            except Employee.DoesNotExist:
                ticket.employee = Employee.objects.get(id=0)
                print("Сотрудник с кодом", tic["employee"], "не найдена в базе данных")

            try:
                ticket.client = Client.objects.get(id=tic["client"])
            except Client.DoesNotExist:
                ticket.client = Client.objects.get(id=0)
                print("Клиент с кодом", tic["client"], "не найдена в базе данных")

            ticket.save()
            dt += 2

        return print("Демо данные в таблице Ticket созданы!")
