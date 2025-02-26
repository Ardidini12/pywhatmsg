from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
from import_export.admin import ImportExportModelAdmin
from .models import Contact, MessageTemplate
import pywhatkit as kit
import datetime

def send_birthday_messages(modeladmin, request, queryset):
    template = MessageTemplate.objects.filter(template_type='birthday').first()
    if not template:
        messages.error(request, "Birthday message template not found.")
        return

    now = datetime.datetime.now()
    send_hour = now.hour
    send_minute = (now.minute + 1) % 60

    for contact in queryset:
        if contact.birthday == datetime.date.today():
            message = template.content.format(first_name=contact.first_name)
            kit.sendwhatmsg(contact.phone_number, message, send_hour, send_minute)
            messages.success(request, f"Scheduled birthday message for {contact.first_name}.")

send_birthday_messages.short_description = "Send Birthday Messages"

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'birthday')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    actions = [send_birthday_messages]
    change_list_template = "admin/contacts_change_list.html"

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and 'send_birthday' in request.POST:
            return self.handle_birthday_action(request)
        
        today = datetime.date.today()
        birthdays = Contact.objects.filter(
            birthday__month=today.month,
            birthday__day=today.day
        )
        extra_context = extra_context or {}
        extra_context['birthdays_today'] = birthdays
        return super().changelist_view(request, extra_context=extra_context)

    def handle_birthday_action(self, request):
        contact_ids = request.POST.getlist('contact_ids')
        if not contact_ids:
            messages.error(request, "No contacts selected!")
            return redirect(request.path)
        
        contacts = Contact.objects.filter(id__in=contact_ids)
        template = MessageTemplate.objects.filter(template_type='birthday').first()
        
        if not template:
            messages.error(request, "Birthday template not found!")
            return redirect(request.path)

        now = datetime.datetime.now()
        send_hour = now.hour
        send_minute = (now.minute + 1) % 60
        
        for contact in contacts:
            try:
                message = template.content.format(first_name=contact.first_name)
                kit.sendwhatmsg(contact.phone_number, message, send_hour, send_minute)
                messages.success(request, f"Message scheduled for {contact.first_name} at {send_hour}:{send_minute:02}")
            except Exception as e:
                messages.error(request, f"Failed to send to {contact.first_name}: {str(e)}")
        
        return redirect(request.path)

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_type', 'content')
    search_fields = ('template_type',)

