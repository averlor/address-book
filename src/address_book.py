import sys
import os
import pickle
import openpyxl
from openpyxl.styles import Alignment

class Person:

    def __init__(self, id, name, familyname, lastname, address, phone):
        self.id = id
        self.name = name
        self.familyname = familyname
        self.lastname = lastname
        self.address = address
        self.phone = phone


def hello_message():
    
    print('''
    Вас приветствует AdBook - портативная адрессная книга.
    Рекомендуем ознакомиться с руководством ниже:
    ''')

def action_print():

    print('''
    Доступные действия:
        1. получить список записей
        2. создать новую запись в адресной книге
        3. обновить запись
        4. удалить запись
        5. сохранить все на диск
        6. выйти
    ''')

def seporator_print():

    print('\n' + '*'*80 + '\n')

def load_order():

    if os.path.exists('log'+os.sep+'address-book.pickle'):
        with open('log'+os.sep+'address-book.pickle', 'rb') as file:
            if not os.stat('log'+os.sep+'address-book.pickle').st_size ==0:
                address_book = pickle.load(file)
    else:
        address_book = [
                    {
                        'id':'№',
                        'name':'ИМЯ',
                        'familyname':'ФАМИЛИЯ',
                        'lastname':'ОТЧЕСТВО',
                        'address':'АДРЕС',
                        'phone':'ТЕЛЕФОН'
                    }
                ]

    return address_book

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

    if (len(address_book) > 1):
        ID = int(address_book[-1]['id']) + 1
    else:
        ID = 1

    ID = str(ID)

    p = Person(ID, name, familyname, lastname, address, phone_re)
    address_book.append(p.__dict__)

def update_order(address_book):
    whom = input('Введите id для обновления: ')
    
    for person in address_book:
        if (whom == person['id']):
            man = person
        else:
            print("\n Человека с таким id не существует!")

    what = input('Что будем менят?(имя, фамилия, отчество, адрес, телефон): ')

    if (what.lower() == 'name' or what.lower() == 'имя'):
        name = input('Введите имя: ')
        man['name'] = name.capitalize()
        print('Данные успешно измененны', man)
    elif (what.lower() == 'familyname' or what.lower() == 'фамилия'):
        familyname = input('Введите фамилию: ')
        man['familyname'] = familyname.capitalize()
        print('Данные успешно измененны', man)
    elif (what.lower() == 'lastname' or what.lower() == 'отчество'):
        lastname = input('Введите отчество: ')
        man['lastname'] = lastname.capitalize()
        print('Данные успешно измененны', man)
    elif (what.lower() == 'address' or what.lower() == 'адрес'):
        address = input('Введите адрес: ')
        man['address'] = address.title()
        print('Данные успешно измененны', man)
    elif (what.lower() == 'phone' or what.lower() == 'телефон'):
        phone = input('Введите телефон: ')
        phone_re = phone[0]+'-(' + phone[1:4] + ')-'+phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
        man['phone'] = phone_re
        print('Данные успешно измененны', man)
    else:
        print('WTF?!')

def delete_order(address_book):
    whom = input('Введите id для удаления: ')
    for person in address_book:
        if (whom == person['id']):
            idx = address_book.index(person)
            del address_book[idx]

    print('\nЗапись удалена\n')

def save(address_book):
    # pickle
    with open('log' + os.sep + 'address-book.pickle', 'wb') as file:
        pickle.dump(address_book, file)

    # file
    try:
        f = open('log' + os.sep + 'address-book.txt', 'w')
        for address in address_book:
            person = address['id'] + '\t' + address['name'] + '\t' + address['familyname'] + '\t' + address['lastname'] + '\t' + address['address'] + '\t' + address['phone'] + '\n'
            f.write(person)
    except KeyboardInterrupt:
        print('\nЗапись не завершена\n')

    finally:
        f.close()

    # excel
    wb = openpyxl.Workbook()
    sheet = wb.create_sheet(index=0, title='Address Book')
    sheet['A1'] = '№'
    sheet['B1'] = 'Имя'
    sheet['C1'] = 'Фамилия'
    sheet['D1'] = 'Отчество'
    sheet['E1'] = 'Адрес'
    sheet['F1'] = 'Телефон'

    
    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        for j in range(1, 2001):
            sheet[i+str(j)].alignment = Alignment(horizontal='center')


    wb.save('log' + os.sep + 'address-book.xlsx')


    print('\nДанные успешно записаны\n')

def exit():
    print('\nДо встречи!\n')
    sys.exit(0)


def main():
    
    address_book = load_order()
    IS_LOOP = True

    while IS_LOOP:

        hello_message()
        action_print()
        seporator_print()

        actions = input('Выберите номер действия: ')

        if (actions == '1'):
            if address_book:
                get_order(address_book)
            else:
                print('\nЕще нет записей в адресной книге\n')

        elif (actions == '2'):
            create_order(address_book)

        elif (actions == '3'):
            if address_book:
                update_order(address_book)
            else:
                print('\nЕще нет записей в адресной книге\n')
            
        elif (actions == '4'):
            delete_order(address_book)

        elif (actions == '5'):
            save(address_book)

        elif (actions == '6'):
            exit()

        else:
            print('\nВы ввели некорректный номер действия\n')
        

if __name__ == '__main__':

    main()