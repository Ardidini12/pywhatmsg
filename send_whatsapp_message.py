import pywhatkit as kit
import datetime
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from messaging.models import Contact, MessageTemplate

def send_birthday_message(contact):
    # Fetch the birthday template
    try:
        template = MessageTemplate.objects.get(template_type='birthday')
    except MessageTemplate.DoesNotExist:
        print("Birthday template not found!")
        return

    # Format the message (you could add more formatting logic)
    message = template.content.format(first_name=contact.first_name)

    # For demonstration, schedule the message 1 minute from now
    now = datetime.datetime.now()
    send_hour = now.hour
    send_minute = (now.minute + 1) % 60

    print(f"Scheduling message to {contact.first_name} at {send_hour}:{send_minute}")
    kit.sendwhatmsg(contact.phone_number, message, send_hour, send_minute)

if __name__ == '__main__':
    # Example: send a birthday message to the first contact in the database
    contact = Contact.objects.first()
    if contact:
        send_birthday_message(contact)
    else:
        print("No contacts available.")
