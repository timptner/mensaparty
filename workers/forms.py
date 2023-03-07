import re

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Template, Context
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from markdown import markdown
from mensaparty import forms
from workers.models import Worker


class UserCreationForm(BaseUserCreationForm):
    password1 = None
    password2 = None

    class Meta:
        model = User
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['first_name', 'last_name', 'email']:
            self.fields[field].required = True

    @staticmethod
    def send_mail(context, recipient):
        msg = loader.render_to_string('admin/auth/mail/set_password.md', context=context)
        email = EmailMultiAlternatives(
            subject="Passwort für neuen Account festlegen",
            body=msg,
            from_email=None,
            to=[recipient],
        )
        email.attach_alternative(markdown(msg), 'text/html')
        email.send()

    def save(self, request, commit=True):
        self.cleaned_data['password1'] = None
        user = super().save(commit=False)
        user.set_unusable_password()
        user.is_staff = True
        if commit:
            user.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()

        groups = Group.objects.filter(name__in=['Beobachter'])
        user.groups.set(groups)

        current_site = get_current_site(request)
        context = {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': current_site.domain,
            'token': default_token_generator.make_token(user),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        }
        self.send_mail(context, user.email)
        return user


class WorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'faculty' in self.fields.keys():
            faculty_choices = [('', '--- Auswählen ---')] + sorted(Worker.FACULTY_CHOICES, key=lambda v: v[1])
            self.fields['faculty'].choices = faculty_choices

        # if 'is_barkeeper' in self.fields.keys():
            # self.fields['is_barkeeper'] = 'Nein'
            # self.fields['is_barkeeper'].required = True

    class Meta:
        model = Worker
        exclude = []
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input"}),
            'last_name': forms.TextInput(attrs={'class': "input"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'phone': forms.TextInput(attrs={'class': "input"}),
            'is_barkeeper': forms.RadioSelect(choices=[(True, "Ja"), (False, "Nein")]),
            'experience': forms.Textarea(attrs={
                'class': "textarea",
                'placeholder': """z. Bsp.
\"6 Jahre als Barkeeper in der Uni-Theke gearbeitet\"
\"Kellnerin bei Peter Pane\"
\"Kann 10 Maßkrüge gleichzeitig tragen\"
\"Ex-Saftschubse bei AirBerlin\"
\"Ich würde gerne die letzte Schicht machen\"
\"Am liebsten bitte Bar/Runner/...\"
""",
            }),
            'strength': forms.NumberInput(attrs={'class': "input"}),
            'available_since': forms.TimeInput(attrs={'class': "input", 'type': 'time'}),
            'available_until': forms.TimeInput(attrs={'class': "input", 'type': 'time'}),
        }
        help_texts = {
            'email': "Es sind nur E-Mail-Adressen der Otto-von-Guericke-Universität Magdeburg erlaubt.",
            'phone': "Bitte gib deine Mobilnummer inklusive <a href=\"https://de.wikipedia.org/wiki/Internationale_"
                     "Telefonvorwahl\" target=\"_blank\">Ländercode</a> an.",
            'strength': "Wie viel kannst du hochheben? Bitte in Kilogram angeben. "
                        "Eine Schätzung reicht aus.",
            'is_barkeeper': "Keine Auswahl gilt als \"Nein\".",
            'available_since': "Bei keiner Angabe wird von flexibler Startzeit ausgegangen.",
            'available_until': "Bei keiner Angabe wird von flexibler Endzeit ausgegangen. Die Angabe einer Endzeit "
                               "ist mit dem Verlassen des Veranstaltungsgeländes gleichzusetzen.",
        }

    def clean_phone(self):
        value = self.cleaned_data['phone']

        value = value.replace(' ', '')

        if value.startswith('00'):
            value = value.replace('00', '+', 1)

        if not value.startswith('+'):
            raise ValidationError("Es wurde keine Ländercode (z. Bsp. +49) angegeben.")

        return value

    def clean_strength(self):
        value = self.cleaned_data['strength']

        if value < 5:
            raise ValidationError("Komm schon! Etwas mehr geht bestimmt. (Die Zahl ist zu klein.)")

        if value > 100:
            raise ValidationError("Bist du es, Hulk? (Die Zahl ist zu groß.)")

        return value


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    recipients = forms.CharField(widget=forms.HiddenInput(), required=True)
    subject = forms.CharField(label="Betreff", max_length=50, required=True)
    message = forms.CharField(
        label="Nachricht",
        widget=forms.Textarea(attrs={
            'placeholder': "Hallo {{ name }},\n\n"
                           "wir freuen uns über Dein Bewerbung als Helfer! Hier kommen die ersten Informationen für "
                           "Deine weitere Planung! Wir treffen uns für eine Besprechung am ...\n\n"
                           "Beste Grüße\n"
                           "ORGA-Team Mensaparty"
        }),
        help_text="Verwende <a href=\"https://www.markdownguide.org/basic-syntax/\">Markdown</a> zur Formatierung.",
        required=True,
    )

    def clean_recipients(self):
        data = self.cleaned_data['recipients']
        if data:
            match = re.fullmatch(r'[\d\s,]+', data)
            if not match:
                raise ValidationError("Nur Zahlen und Kommata sind erlaubt.")
        return data

    def clean_message(self):
        data = self.cleaned_data['message']
        if data:
            if '{{ name }}' not in data:
                raise ValidationError("Du hast <code>{{ name}}</code> in der Nachricht nicht verwendet!")
        return data

    def send_mail(self, request):
        recipients = self.cleaned_data['recipients']
        recipient_list = [recipient.strip() for recipient in recipients.split(',')]
        workers = Worker.objects.filter(pk__in=recipient_list)

        message = self.cleaned_data['message']
        signature = loader.render_to_string('mail/_signature.md')

        email_list = []
        for worker in workers:
            context = Context({'name': worker.first_name})
            body = Template(message).render(context)
            body += '\n\n' + signature

            email = EmailMultiAlternatives(
                subject="Neue Nachricht zur Mensaparty",
                body=body,
                from_email='mensaparty-batch@farafmb.de',
                to=[worker.email],
            )
            email.attach_alternative(markdown(body), 'text/html')
            email.esp_extra = {'MessageStream': 'broadcast'}
            email_list.append(email)

        connection = mail.get_connection()
        connection.send_messages(email_list)

        amount = len(email_list)
        if amount == 1:
            msg = f"Erfolgreich {amount} Helfer eine E-Mail geschickt."
        else:
            msg = f"Erfolgreich {amount} Helfern eine E-Mail geschickt."

        messages.success(request, msg)
