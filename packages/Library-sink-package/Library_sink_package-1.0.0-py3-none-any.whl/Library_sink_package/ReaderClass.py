class Reader:
    AllReaders = [('Oleg', 'Petrov', 23), ('Maxim', 'Ivanov', 33), ('Olga', 'Andriivna', 18)]
    def __init__(self, name, secondname, age):
        self.name = name
        self.secondname = secondname
        self.age = age



    def newReader(self):
        newReader = (input('Your name:'), input('Your secondname:'), input('Your age:'))
        return Reader.AllReaders.append(newReader)
