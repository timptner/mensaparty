from django import forms
from django.core.exceptions import ValidationError
from workers.models import Worker


class WorkerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        faculty_choices = [('', '--- Auswählen ---')] + sorted(Worker.FACULTY_CHOICES, key=lambda v: v[1])
        self.fields['faculty'].choices = faculty_choices

    class Meta:
        model = Worker
        exclude = []
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input"}),
            'last_name': forms.TextInput(attrs={'class': "input"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'phone': forms.TextInput(attrs={'class': "input"}),
            'experience': forms.Textarea(attrs={
                'class': "textarea",
                'placeholder': """z. Bsp.

\"6 Jahre als Barkeeper in der Uni-Theke gearbeitet\"

\"Kellnerin bei Peter Pane\"

\"Kann 10 Maßkrüge gleichzeitig tragen\"

\"Ex-Saftschubse bei AirBerlin\"
""",
            }),
            'strength': forms.NumberInput(attrs={'class': "input"}),
        }
        help_texts = {
            'phone': "Bitte gib deine Mobilnummer inklusive <a href=\"https://de.wikipedia.org/wiki/Internationale_"
                     "Telefonvorwahl\" target=\"_blank\">Ländercode</a> an.",
            'strength': "Wie viel kannst du hochheben? Bitte in Kilogram angeben. "
                        "Eine Schätzung reicht aus."
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
