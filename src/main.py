# includes class
from Book import Book

def main():

    '''Main function'''

    book = Book()
    address_book = book.load_order()

    IS_LOOP = True

    while IS_LOOP:

        book.hello_message()
        book.action_message()
        book.separation_print()

        actions = input('Выберите номер действия: ')

        if (actions == '1'):
            if address_book:
                book.get_order(address_book)
            else:
                print('\nЕще нет записей в адресной книге\n')

        elif (actions == '2'):
            book.create_order(address_book)

        elif (actions == '3'):
            if address_book:
                book.update_order(address_book)
            else:
                print('\nЕще нет записей в адресной книге\n')

        elif (actions == '4'):
            book.delete_order(address_book)

        elif (actions == '5'):
            book.save(address_book)

        elif (actions == '6'):
            book.exit()

        else:
            print('\nВы ввели некорректный номер действия\n')

if __name__ == '__main__':

    main()