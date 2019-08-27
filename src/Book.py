import sys
import os
import pickle
import datetime
import sqlite3 as db

from Person import Person

class Book:

    params = ['id', 'name', 'familyname', 'lastname', 'address', 'phone', 'datecreate', 'datemodify']
    address_book_for_bd = []

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
                5. сохранить все на диск(рекомендуется)
                6. выйти
            ''')

    def separation_print(self):

        print('\n' + '*' * 80 + '\n')

    def load_order(self):

        '''Loader data'''

        conn = None

        try:
            conn = db.connect('db' + os.sep + 'address_book.db')
            cursor = conn.cursor()

            sql = "SELECT * FROM adress_book"
            try:
                cursor.execute(sql)
            except db.Error as err:
                print(err)

            address_book = cursor.fetchall()

        except db.Error as err:
            print("Ошибка при работе с БД...")
            print(sys.exc_info()[1])

        finally:
            if conn:
                conn.close()

            else:

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

        # print(address_book)

        for person in address_book:

            if isinstance(person, tuple):
                person = dict(zip(self.params, list(person)))

            pers = str(person['id']) + '    ' + person['name'] + '    ' + person['familyname'] + '    ' + person[
                'lastname'] + '    ' + person['address'] + '    ' + person[
                'phone'] + '    ' + person['datecreate'] + '    ' + person['datemodify']
            print('{:^100}'.format(str(pers)))

    def find(self, address_book):
        pass

    def create_order(self, address_book):

        '''Create order in address book'''

        name = input('Введите имя человека: ').capitalize()
        familyname = input('Введите фамилию человека: ').capitalize()
        lastname = input('Введите отчество человека: ').capitalize()
        address = input('Введите адрес человека: ').title()
        phone = input('Введите телефон человека(89009998877): ')
        phone_re = phone[0] + '-(' + phone[1:4] + ')-' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
        date_create = datetime.datetime.now().strftime("%d-%m-%Y")
        date_modify = datetime.datetime.now().strftime("%d-%m-%Y")

        if isinstance(address_book[-1], tuple):
            last_item = dict(zip(self.params, list(address_book[-1])))
            ID = last_item['id'] + 1

        else:
            if (len(address_book) > 1):
                ID = int(address_book[-1]['id']) + 1
            else:
                ID = 1

        p = Person(ID, name, familyname, lastname, address, phone_re,
                   date_create, date_modify)
        address_book.append(p.__dict__)

        self.address_book_for_bd.append((p.id, p.name, p.familyname, p.lastname, p.address, p.phone, p.datecreate,
                                    p.datemodify))

    # FIXME: fix error
    def update_order(self, address_book):

        '''Update order from address book'''

        whom = int(input('Введите id для обновления: '))

        for person in address_book:

            if isinstance(person, tuple):
                person = dict(zip(self.params, list(person)))

            print(person)

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

    # FIXME: fix error
    def delete_order(self, address_book):

        '''Delete order from address book'''

        whom = int(input('Введите id для удаления: '))
        for person in address_book:

            if isinstance(person, tuple):
                person = dict(zip(self.params, list(person)))

            if (whom == person['id']):

                try:
                    conn = db.connect('db' + os.sep + 'address_book.db')
                    cursor = conn.cursor()

                    sql = "DELETE FROM adress_book WHERE id = ?"
                    try:
                        cursor.execute(sql, tuple(whom))
                        conn.commit()
                    except db.Error as err:
                        print(err)

                    address_book = cursor.fetchall()

                except db.Error as err:
                    print(err)
                    if conn:
                        conn.rollback()

                finally:
                    if conn:
                        conn.close()

                idx = address_book.index(person)
                del address_book[idx]

        print('\nЗапись удалена\n')

    def save(self, address_book):

        try:
            conn = db.connect('db' + os.sep + 'address_book.db')
            cursor = conn.cursor()

            sql = "INSERT INTO adress_book VALUES(?,?,?,?,?,?,?,?)"
            try:
                cursor.executemany(sql, self.address_book_for_bd)
                conn.commit()
            except db.Error as err:
                print(err)
                if conn:
                    conn.rollback()

        except db.Error as err:
            print("Ошибка при работе с БД...")
            print(sys.exc_info()[1])

        finally:
            if conn:
                conn.close()

        # pickle
        with open('log' + os.sep + 'address-book.pickle', 'wb') as file:
            pickle.dump(address_book, file)

    def exit(self):

        '''Close programm'''

        print('\nДо встречи!\n')
        sys.exit(0)