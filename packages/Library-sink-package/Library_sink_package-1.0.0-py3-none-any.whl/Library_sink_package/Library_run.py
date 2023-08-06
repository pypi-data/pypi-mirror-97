from Library_sink_package import BookClass, ReaderClass
class Library:
    book_list = BookClass.Book.all_default_books
    reader_list = ReaderClass.Reader.AllReaders     # список користувачів за замовчуванням
    now_add_book_list = []                          # список доданих книг
    now_book_in_library = book_list                 # список книг в наявності
    not_book_list = []                              # список книг не в наявності
    all_book_default = BookClass.Book.all_default_books2    # список книг за замовчуванням
    reader_take = []                                # список читач - книга яку взяв
    our_reader_now = []                             # інформація про атовризованого читача
    def show_all_books():
        print('All books which our library have are:')
        [print(str(Library.all_book_default[i])) for i in range(len(Library.all_book_default))]

    def show_now_books():
        print('Today our library have the next books:')
        [print(str(Library.now_book_in_library[i])) for i in range(len(Library.now_book_in_library))]

    def show_not_book_now():
        print('Today our library do not have the next books:')
        if len(Library.not_book_list) == 0:
            print("At now this list is empty")
        elif len(Library.not_book_list) == 1:
            print(*Library.not_book_list)
        else:
            [print(str(Library.not_book_list[i])) for i in range(len(Library.not_book_list))]

# Функція знайомства з читачем
    def welcome():
        answer = input('Are you a member of our library? ')
        if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
            print('\nPlease chose your information about you from our reader list:\nAnswer must be more 3 letters.')
            [print(str(Library.reader_list[i])) for i in range(len(Library.reader_list))]
            chose_reader = input('Information about me is:')
            if len(chose_reader) >= 3:
                for i in range(len(Library.reader_list)):
                    if chose_reader.lower() in str(Library.reader_list[i]).lower():
                        print('You are:', Library.reader_list[i], '\n')
                        Library.our_reader_now = Library.reader_list[i]     # призначаэмо в глобальну змінну нашого користувача
            else:
                print('Sorry, your answer must be more 3 letters')
                Library.welcome()
# Додаємо новочго читача до нашого списку читачів
        elif answer == 'n' or answer == 'N' or answer == 'now' or answer == 'Now':
            print('We will append you in our list or reader.\nPlease enter the next information about you')
            Library.our_reader_now = ReaderClass.Reader.newReader('')
            print('Congratulation! You appended in our reader list:\n')
        else:
            print('Sorry, but you entered wrong answer')
            Library.welcome()

# Видаляємо книгу зі списку книг
    def remove_book():
        [print(str(Library.now_book_in_library[i])) for i in range(len(Library.now_book_in_library))]
        our_remove_name_book = BookClass.Book.remove_book_from_all('')
        old_all_books_list = Library.now_book_in_library
        for i in range(len(old_all_books_list)):
            if our_remove_name_book.lower() in str(old_all_books_list[i]).lower():
                print('You remove the next book:', old_all_books_list[i])
                Library.not_book_list += [old_all_books_list[i]]
                old_all_books_list.remove(old_all_books_list[i])
                break
        Library.now_book_in_library = old_all_books_list

# Функція для повтору запиту у читача для подальших дій
    def repeat_choose():
        repeat = input('\nDo you want something else?')
        if repeat == 'y' or repeat == 'yes' or repeat == 'Yes' or repeat == 'Y':
            list_user_chose_lambda()
            Library.user_chose()
        else:
            print('Ok, good bye')
            exit()

# Отримання книги з бібліотеки
    def reader_take_book():
        [print(str(Library.now_book_in_library[i])) for i in range(len(Library.now_book_in_library))]
        take_book_name = BookClass.Book.name_wanted_book('')
        old_all_book_list = Library.now_book_in_library
        for i in range(len(old_all_book_list)):
            if take_book_name.lower() in str(old_all_book_list[i]).lower():
                print('You want to take the next book:', old_all_book_list[i])
                reader_name_book = Library.our_reader_now, old_all_book_list[i]     # створюємо список з двох елементів type typle
                Library.reader_take += [reader_name_book]
                remove_name_book = old_all_book_list[i]
                # Виводимо список читачів та книги які вони взяли
                print('Our readers and books which must be returned are:\n', *Library.reader_take)
        Library.now_book_in_library.remove(remove_name_book)
        Library.not_book_list += [remove_name_book]

# Повернення книги у бібліотеку
    def return_book():
        if len(Library.reader_take) == 0:
            print('At now this list is empty')
        else:
            print('Our readers and books which must be return are:', *Library.reader_take)
            name_to_return = BookClass.Book.return_book_in_library('')
            return_book_list = Library.reader_take
            if len(return_book_list) == 0:
                print('At now this list is empty')
            else:
                for i in range(len(return_book_list)):
                    if name_to_return.lower() in str(return_book_list[i]).lower():
                        print('You want to return:', *return_book_list[i])
                        return_book_name = return_book_list[i]

# Видаляє боржника зі списку боржників
                Library.reader_take.remove(return_book_name)

                # Видаляємо дану книгу зі списку книг котрих немає в наявності
                deleted_now_book_list = Library.not_book_list
                for i in range(len(deleted_now_book_list)):
                    if name_to_return.lower() in str(deleted_now_book_list[i]).lower():
                        deleted_book_name = deleted_now_book_list[i]
                Library.not_book_list.remove(deleted_book_name)
                # Добавляємо книгу котру читач повернув
                Library.now_book_in_library.append(deleted_book_name)

# Здійснюємо сортування
    def book_sort():
        Library.now_book_in_library.sort()
        print('You sorted yhe books:')
        [print(str(Library.now_book_in_library[i])) for i in range(len(Library.now_book_in_library))]


    # Функція вибору користувачем дії зі списку
    def user_chose():
        answer_to_do = input('Enter you number:')
# Виводимо всі книги котрі є за замовчуванням у бібліотеці
        if answer_to_do == '1':
            Library.show_all_books()
            Library.repeat_choose()

# Виводимо всі книги котрі є на даний момент у бібліотеці
        elif answer_to_do == '2':
            Library.show_now_books()
            Library.repeat_choose()

# Виводимо всі книги котрих немає у бібліотеці
        elif answer_to_do == '3':
            Library.show_not_book_now()
            Library.repeat_choose()

# Додаємо нову книгу у загальний список книг
        elif answer_to_do == '4':
            BookClass.Book.add_new_book('')
            Library.now_book_in_library += BookClass.Book.add_new_book_list
            print('You add a new book')
            Library.repeat_choose()

# Видаляємо книгу з загального списку книг
        elif answer_to_do == '5':
            print('Now our library have the next books:')
            Library.remove_book()
            Library.repeat_choose()

# Читач забирає книгу з бібліотеки
        elif answer_to_do == '6':
            print('\nOur library have the next books:')
            Library.reader_take_book()
            Library.repeat_choose()

# Повертаємо книгу
        elif answer_to_do == '7':
            Library.return_book()
            Library.repeat_choose()

# Сортуємо книги
        elif answer_to_do == '8':
            Library.book_sort()
            Library.repeat_choose()

# Виходимо з програми
        elif answer_to_do == '0':
            print('Good bye, see you later! ')
            exit()

print('Hello in our library!')
# Дізнаємося чи наш гість є членом бібліотеки чи ні, якщо ні, то додаємо його до нашого списку читачів
Library.welcome()

# Використовуємо Лямбду функцію для виводу на екран списку з діями
list_user_chose_lambda = lambda :print('Please chose the number from our list what do you want to do\n1)-> Please show all books in library\n2)-> Please show books which are in library now\n3)-> Please show books which are not in library now\n4)-> I want to add new book\n5)-> I want to remove book\n6)-> I want to take a book\n7)-> I want to return the book\n8)-> I want to sort the books\n0)-> Exit from library')

# Виводимо список дій через Лямбду функцію
list_user_chose_lambda()
# Вибираємо що читат бажає зробити у нашій бібліотеці
Library.user_chose()
