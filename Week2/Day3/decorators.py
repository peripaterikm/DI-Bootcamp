from datetime import datetime, date

class Person:

    def __init__(self, name, last_name, birth_date):
        self.name = self.format_name(name)
        self.last_name = self.format_name(last_name)
        self.birth_date = self.parse_birthdate(birth_date)

    @classmethod
    def from_age(cls, name, last_name, age):
        current_year = datetime.today().year
        birth_year = current_year - age
        birth_date = f'{birth_year}-1-1'
        return cls(name, last_name, birth_date)

    @staticmethod
    def parse_birthdate(date_string):
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    
    @staticmethod
    def format_name(name_string):
        return name_string.capitalize()

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

p1 = Person('Alice', 'Wonder', '1990-02-05')
print(type(p1.birth_date))  # <class 'datetime.date'>
print(p1.age)

p2 = Person.from_age('Bob', 'Smith', 30)
print(p2.birth_date)
print(p2.name, p2.last_name)

p3 = Person('juliana', 'schmidt', '1989-06-15')
print(p3.name, p3.last_name)  # Juliana Schmidt
