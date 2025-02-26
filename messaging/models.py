from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, help_text="Include country code, e.g., +1234567890")
    email = models.EmailField(blank=True, null=True)
    birthday = models.DateField(help_text="Format: YYYY-MM-DD")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MessageTemplate(models.Model):
    TEMPLATE_CHOICES = (
        ('birthday', 'Happy Birthday'),
        ('receipt', 'Receipt Confirmation'),
    )
    template_type = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, unique=True)
    content = models.TextField(help_text="Message content. For receipt, include placeholder like {receipt_id}")

    def __str__(self):
        return self.get_template_type_display()

