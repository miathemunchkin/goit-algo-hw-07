from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y')
                if today.date() <= birthday_date.date() <= (today + timedelta(days=7)).date():
                    upcoming_birthdays.append((record.name.value, birthday_date.strftime('%d.%m.%Y')))
        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return inner


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return f"Contact '{name}' not found."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value}."
    elif record and not record.birthday:
        return f"{name} has no birthday set."
    else:
        return f"Contact '{name}' not found."


@input_error
def birthdays(_, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{name}'s birthday on {birthday}" for name, birthday in upcoming_birthdays])
    else:
        return "No upcoming birthdays."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            # Implementation for adding a contact
            name = args[0]
            record = Record(name)
            if len(args) > 1:
                phones = args[1:]
                for phone in phones:
                    record.add_phone(phone)
            book.add_record(record)
            print(f"Contact {name} added.")

        elif command == "change":
            # Implementation for changing phone number
            pass

        elif command == "phone":
            # Implementation for showing phone number
            pass

        elif command == "all":
            # Implementation for showing all contacts
            for record in book.data.values():
                print(record)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
