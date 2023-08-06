class Book:
    all_default_books = [('Mathematics', 'Decart', 1887), ('History', 'Napoleon', 1899), ('Musik', 'Mocart', 1799), ('Philosofy', 'Solomon', 1865)]
    all_default_books2 = [('Mathematics', 'Decart', 1887), ('History', 'Napoleon', 1899), ('Musik', 'Mocart', 1799), ('Philosofy', 'Solomon', 1865)]
    add_new_book_list = []
    def __init__(self, name, author, year, data):
        self.name = name
        self.author = author
        self.year =year
        self.data = data

    def name_wanted_book(self):
        reader_want_book = input('Please, enter information about the book which you want to take:')
        return reader_want_book

    def add_new_book(self):
        book_add = (input("Book's name:"), input("Author's name"), int(input("Book's year:")))
        return Book.add_new_book_list.append(book_add)

    def remove_book_from_all(self):
        remove_name_book = input('Enter the name of book which you want to remove:')
        return remove_name_book

    def return_book_in_library(self):
        reader_return_book = input('Please, enter information about the book which you want to take:')
        return reader_return_book



