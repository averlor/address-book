class Person:

    id = 0

    def __init__(self, id, name, familyname, lastname, address, phone):
        self.id = id
        self.name = name
        self.familyname = familyname
        self.lastname = lastname
        self.address = address
        self.phone = phone


def get_order(address_book):
    for person in address_book:
        pers = person['id'] + '    ' + person['name'] + '    ' + person['familyname'] + '    ' + person['lastname'] + '    ' + person['address'] + '    ' + person['phone']
        print('{:^100}'.format(str(pers)))
        
def create_order(address_book):
    name = input('Введите имя человека: ').capitalize()
    familyname = input('Введите фамилию человека: ').capitalize()
    lastname = input('Введите отчество человека: ').capitalize()
    address = input('Введите адрес человека: ').title()
    phone = input('Введите телефон человека(89009998877): ')
    phone_re = phone[0]+'-(' + phone[1:4] + ')-'+phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]

    Person.id += 1
    ID = str(Person.id)

    p = Person(ID, name, familyname, lastname, address, phone_re)
    address_book.append(p.__dict__)

def update_order(address_book):
    whom = input('Введите id для обновления: ')
    for person in address_book:
        if (whom == person.id):
            man = person
        else:
            print("\n Человека с таким id не существует!")

    what = input('Что будем менят?(имя, фамилия, отчество, адрес, телефон): ')

    if (what.lower() == 'name' or what.lower() == 'имя'):
        name = input('Введите имя: ')
        man['name'] = name
        print('Данные успешно измененны', man)
    elif (what.lower() == 'familyname' or what.lower() == 'фамилия'):
        familyname = input('Введите фамилию: ')
        man['familyname'] = familyname
        print('Данные успешно измененны', man)
    elif (what.lower() == 'lastname' or what.lower() == 'отчество'):
        lastname = input('Введите отчество: ')
        man['lastname'] = lastname
        print('Данные успешно измененны', man)
    elif (what.lower() == 'address' or what.lower() == 'адрес'):
        address = input('Введите адрес: ')
        man['address'] = address
        print('Данные успешно измененны', man)
    elif (what.lower() == 'phone' or what.lower() == 'телефон'):
        phone = input('Введите адрес: ')
        man['phone'] = phone
        print('Данные успешно измененны', man)
    else:
        print('WTF?!')



if __name__ == '__main__':

    address_book = []

    print('''
    Вас приветствует AdBook - портативная адрессная книга.
    Рекомендуем ознакомиться с руководством ниже:
        1. получить список записей
        2. создать новую запись в адресной книге
        3. обновить запись
        4. удалить запись
        5. сохранить все на диск
        6. выйти
    ''')

    create_order(address_book)

    get_order(address_book)

    update_order(address_book)

    print(address_book)