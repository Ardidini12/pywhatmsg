import csv
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from messaging.models import Contact

def import_contacts(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contact, created = Contact.objects.get_or_create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone_number=row['phone_number'],
                email=row.get('email'),
                birthday=row['birthday']
            )
            if created:
                print(f"Imported {contact}")
            else:
                print(f"{contact} already exists")

if __name__ == '__main__':
    import_contacts('contacts.csv')
