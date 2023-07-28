from collections import UserDict
import csv
import os
import re

class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]

    def show_all_records(self):
        if not self.data:
            print("[-] No records found in the address book.")
        else:
            for name, record in self.items():
                print('#' + '-' * 30)
                print(f'Name:   {name}')
                phones_str = "; ".join([f"[{i + 1}] {phone.value}" for i, phone in enumerate(record.phones)])
                print(f'Phones: {phones_str}')

    def search_record(self):
        pass

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for record in self.data.values():
                phones_list = [phone.value for phone in record.phones]
                writer.writerow({'Name': record.name.value, 'Phone': phones_list})

    def load_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                name = row['Name']
                phones_str = row['Phone']
                phones_list = eval(phones_str)
                record = Record(name)
                for phone in phones_list:
                    record.add_phone(phone)
                self.add_record(record)

class Bot:
    def __init__(self, address_book):
        self.address_book = address_book
        self.contact_data = self.address_book.data

    def handle_hello(self, *args):
        print("[+] Hi, I am Cortana and I am here to help! A touch of sign in here and a WiFi there... Just kidding! I am Based Assistant :)\nType in 'help' if you feel lost or press 'CTRL+C' to exit. Enough intro let's dig in...")

    def handle_help(self, *args):
        print("[+] Supported Commands:"
              "\n0 or help      " "Show help message."
              "\n1 or add       " "Add new record."
              "\n2 or delete    " "Delete record."
              "\n3 or change    " "Change existing record."
              "\n4 or add phone " "Add extra phone."
              "\n5 or show all  " "Show all records."
              "\n6 or q         " "Exit."
              "\n6 or close     " "Exit."
              "\n6 or exit      " "Exit."
              "\n6 or quit      " "Exit."
              "\nphone          " "Show contact phone (ex.: 'phone John')."
              "\nhello          " "Print a greeting.")

    def handle_add(self):
        while True:
            name = input("Enter a new name: ")
            if not name:
                print("[-] Error: Name cannot be empty. Please try again.")
            elif name in self.address_book.data:
                print(f"[-] Error: '{name}' already exists in the address book.")
            else:
                break
        record = Record(name)
        phone = input("Enter a new phone: ")
        record.add_phone(phone)
        self.address_book.add_record(record)
        print("[+] Record added successfully!")

    def handle_delete(self):
        name = input("Enter a name to delete: ")
        self.address_book.delete_record(name)
        print(f"[+] '{name}' record deleted successfully!")

    def handle_change(self):
        name = input("Enter a name to edit: ")
        record = self.address_book.data.get(name)
        if not record:
            print(f"[-] '{name}' record not found.")
            return

        print(f"\nSelect a field to edit for '{name}':")
        print("1. Name")
        print("2. Phone")
        choice = input("Chose a field to edit (1/2): ")

        if choice == '1':
            new_name = input("Enter a new name: ")
            if not new_name:
                print("[-] Error: Name cannot be empty. Please try again.")
            else:
                self.address_book.delete_record(name)
                record.name.value = new_name
                self.address_book.add_record(record)
                print("[+] Name changed.")
        elif choice == '2':
            if len(record.phones) == 1:
                new_phone = input("Enter a new phone number: ")
                if new_phone in [phone.value for phone in record.phones]:
                    print("[-] This phone number already exists for this contact.")
                else:
                    record.phones[0].value = new_phone
                    print("[+] Phone edited successfully!")
            elif len(record.phones) > 1:
                print(f"'{name}' phones:")
                for index, phone in enumerate(record.phones, 1):
                    print(f"{index}. {phone.value}")
                phone_index = input("Enter the index of the phone number to edit: ")
                try:
                    phone_index = int(phone_index)
                    if 1 <= phone_index <= len(record.phones):
                        new_phone = input("Enter the new phone number: ")
                        if new_phone in [phone.value for phone in record.phones]:
                            print("[-] This phone number already exists for this contact.")
                        else:
                            record.edit_phone(record.phones[phone_index - 1].value, new_phone)
                            print("[+] Phone edited successfully!")
                    else:
                        print("[-] Invalid input. Please try again.")
                except ValueError:
                    print("[-] Invalid input. Please enter a valid number.")
            else:
                print(f"[-] No phone numbers found for '{name}'.")
        else:
            print("[-] Invalid input. Please try again.")

    def handle_add_phone(self):
        name = input("Enter a name: ")
        record = self.address_book.data.get(name)
        if not record:
            print(f"[-] '{name}' record not found.")
            return
        while True:
            phone = input("Enter a phone number (type 'done' to finish): ")
            if phone.lower() == 'done':
                break
            if phone in [p.value for p in record.phones]:
                print("[-] This phone number already exists for this contact.")
            else:
                record.add_phone(phone)
        print("[+] Phone number(s) added.")

    def handle_delete_phone(self):
        name = input("Enter a name: ")
        record = self.address_book.data.get(name)
        if not record:
            print(f"[-] '{name}' record not found.")
            return
        if len(record.phones) == 1:
            phone = record.phones[0].value
            record.delete_phone(phone)
            print("[+] Phone number deleted.")
        elif len(record.phones) > 1:
            print(f"'{name}' phones:")
            for index, phone in enumerate(record.phones, 1):
                print(f"{index}. {phone.value}")
            phone_index = input("Enter the index of the phone number to delete: ")
            try:
                phone_index = int(phone_index)
                if 1 <= phone_index <= len(record.phones):
                    phone = record.phones[phone_index - 1].value
                    record.delete_phone(phone)
                    print("[+] Phone number deleted.")
                else:
                    print("[-] Invalid input. Please try again.")
            except ValueError:
                print("[-] Invalid input. Please enter a valid number.")
        else:
            print(f"[-] No phone numbers found for '{name}'.")

    def handle_show_all(self):
        self.address_book.show_all_records()

    def handle_phone(self, *args):
        name = input("Enter a name to search: ")
        record = self.address_book.data.get(name)
        if not record:
            print(f"[-] '{name}' record not found.")
            return
        print(f"'{name}' phones:")
        index = 1
        for phone in record.phones:
            print(f"{index}. {phone.value}")
            index += 1

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("[+] Hi, I am Cortana and I am here to help! A touch of sign in here and a WiFi there... Just kidding! I am Based Assistant :)\nType in 'help' if you feel lost or press 'CTRL+C' to exit. Enough intro let's dig in...")
        while True:
            print('\n#' + '-' * 30)
            print("What would you like to do?")
            print("0. Help")
            print("1. Add a record")
            print("2. Delete a record")
            print("3. Edit a record")
            print("4. Add phone(s)")
            print("5. Delete phone")
            print("6. Show all records")
            print("7. Exit")
            choice = input("Enter your choice (1/2/3/4/5/6/7): ").lower()

            if choice in ('0', 'help'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_help()
            elif choice in ('1', 'add'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_add()
            elif choice in ('2', 'delete'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_delete()
            elif choice in ('3', 'change'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_change()
            elif choice in ('4', 'add phone'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_add_phone()
            elif choice in ('5', 'delete phone'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_delete_phone()
            elif choice in ('6', 'show all'):
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_show_all()
            elif choice in ('7', 'exit', 'close', 'quit', 'q'):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("[+] See you later, Pal.")
                break
            elif choice == 'hello':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_hello()
            elif choice == 'phone':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.handle_phone()
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("[-] Invalid choice. Try again.")

def main():
    if not os.path.exists('contacts.csv'):
        with open('contacts.csv', 'w', newline=''):
            pass
    address_book = AddressBook()
    address_book.load_from_csv('contacts.csv')
    bot = Bot(address_book)
    try:
        bot.run()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        pass
    finally:
        address_book.save_to_csv('contacts.csv')


if __name__ == '__main__':
    main()
