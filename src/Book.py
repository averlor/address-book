import sys
import os
import pickle
import datetime
import sqlite3 as db

import openpyxl
from openpyxl.styles import Alignment

from Person import Person

class Book:

    def hello_message(self):

        '''Hello message'''

        print('''
            Вас приветствует AdBook - портативная адрессная книга.
            Рекомендуем ознакомиться с руководством ниже:
            ''')

    def action_message(self):

        '''Message of actions'''

        print('''
            Доступные действия:
                1. получить список записей
                2. создать новую запись в адресной книге
                3. обновить запись
                4. удалить запись
                5. сохранить все на диск
                6. выйти
            ''')

    def separation_print(self):

        print('\n' + '*' * 80 + '\n')

    # FIXME: added connect to db
    def load_order(self):

        '''Loader data'''

        conn = db.connect('db' + os.sep + 'address_book.db')
        cursor = conn.cursor()

        sql = "SELECT * FROM adress_book"
        cursor.execute(sql)

        address_book = cursor.fetchall()
        print(type(address_book))

        if (len(address_book) == 0):

            if os.path.exists('log' + os.sep + 'address-book.pickle'):
                with open('log' + os.sep + 'address-book.pickle', 'rb') as file:
                    if not os.stat('log' + os.sep + 'address-book.pickle').st_size == 0:
                        address_book = pickle.load(file)
            else:
                address_book = [
                    {
                        'id': '№',
                        'name': 'ИМЯ',
                        'familyname': 'ФАМИЛИЯ',
                        'lastname': 'ОТЧЕСТВО',
                        'address': 'АДРЕС',
                        'phone': 'ТЕЛЕФОН',
                        'datecreate': 'Дата создания',
                        'datemodify': 'Дата обновления'
                    }
                ]

        return address_book

    def get_order(self, address_book):

        '''Get list of order'''

        for person in address_book:
            pers = person['id'] + '    ' + person['name'] + '    ' + person['familyname'] + '    ' + person[
                'lastname'] + '    ' + person['address'] + '    ' + person[
                'phone'] + '    ' +  person['datecreate'] + '    ' + person['datemodify']
            print('{:^100}'.format(str(pers)))

    def create_order(self, address_book):

        '''Create order in address book'''

        name = input('Введите имя человека: ').capitalize()
        familyname = input('Введите фамилию человека: ').capitalize()
        lastname = input('Введите отчество человека: ').capitalize()
        address = input('Введите адрес человека: ').title()
        phone = input('Введите телефон человека(89009998877): ')
        phone_re = phone[0] + '-(' + phone[1:4] + ')-' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
        date_create = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        date_modify = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

        if (len(address_book) > 1):
            ID = int(address_book[-1]['id']) + 1
        else:
            ID = 1

        ID = str(ID)

        p = Person(ID, name, familyname, lastname, address, phone_re,
                   date_create, date_modify)
        address_book.append(p.__dict__)

    def update_order(self, address_book):

        '''Update order from address book'''

        whom = input('Введите id для обновления: ')

        for person in address_book:
            if (whom == person['id']):
                man = person

                what = input('Что будем менят?(имя, фамилия, отчество, адрес, телефон): ')

                if (what.lower() == 'name' or what.lower() == 'имя'):
                    name = input('Введите имя: ')
                    man['name'] = name.capitalize()
                    man['datemodify'] = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
                    print('Данные успешно измененны', man)
                elif (what.lower() == 'familyname' or what.lower() == 'фамилия'):
                    familyname = input('Введите фамилию: ')
                    man['familyname'] = familyname.capitalize()
                    man['datemodify'] = datetime.datetime.now().strftime(
                        "%A, %d. %B %Y %I:%M%p")
                    print('Данные успешно измененны', man)
                elif (what.lower() == 'lastname' or what.lower() == 'отчество'):
                    lastname = input('Введите отчество: ')
                    man['lastname'] = lastname.capitalize()
                    man['datemodify'] = datetime.datetime.now().strftime(
                        "%A, %d. %B %Y %I:%M%p")
                    print('Данные успешно измененны', man)
                elif (what.lower() == 'address' or what.lower() == 'адрес'):
                    address = input('Введите адрес: ')
                    man['address'] = address.title()
                    man['datemodify'] = datetime.datetime.now().strftime(
                        "%A, %d. %B %Y %I:%M%p")
                    print('Данные успешно измененны', man)
                elif (what.lower() == 'phone' or what.lower() == 'телефон'):
                    phone = input('Введите телефон: ')
                    phone_re = phone[0] + '-(' + phone[1:4] + ')-' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
                    man['phone'] = phone_re
                    man['datemodify'] = datetime.datetime.now().strftime(
                        "%A, %d. %B %Y %I:%M%p")
                    print('Данные успешно измененны', man)
                else:
                    print('WTF?!')

            else:
                print("\n Человека с таким id не существует!")

    def delete_order(self, address_book):

        '''Delete order from address book'''

        whom = input('Введите id для удаления: ')
        for person in address_book:
            if (whom == person['id']):
                idx = address_book.index(person)
                del address_book[idx]

        print('\nЗапись удалена\n')

    # FIXME: added connect to db
    def save(self, address_book):

        '''Save changes'''

        # pickle
        with open('log' + os.sep + 'address-book.pickle', 'wb') as file:
            pickle.dump(address_book, file)

        # file
        try:
            f = open('log' + os.sep + 'address-book.txt', 'w')
            for address in address_book:
                person = address['id'] + '\t' + address['name'] + '\t' + address['familyname'] + '\t' + address[
                    'lastname'] + '\t' + address['address'] + '\t' + address[
                    'phone'] + '\t\t' + address['datecreate'] + '\t\t' + \
                         address[
                    'datemodify'] + '\n'
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
        sheet['G1'] = 'Дата создания'
        sheet['H1'] = 'Дата обновления'

        for i in ['A', 'B', 'C', 'D', 'E', 'F']:
            for j in range(1, 2001):
                sheet[i + str(j)].alignment = Alignment(horizontal='center')

        wb.save('log' + os.sep + 'address-book.xlsx')

        print('\nДанные успешно записаны\n')

    def exit(self):

        '''Close programm'''

        print('\nДо встречи!\n')
        sys.exit(0)