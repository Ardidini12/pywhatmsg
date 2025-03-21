# Generated by Django 5.1.6 on 2025-02-26 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(help_text='Include country code, e.g., +1234567890', max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateField(help_text='Format: YYYY-MM-DD')),
            ],
        ),
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('birthday', 'Happy Birthday'), ('receipt', 'Receipt Confirmation')], max_length=20, unique=True)),
                ('content', models.TextField(help_text='Message content. For receipt, include placeholder like {receipt_id}')),
            ],
        ),
    ]
