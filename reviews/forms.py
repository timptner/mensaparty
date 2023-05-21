from django import forms
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = []
        labels = {
            'rating': "Gesamt-Bewertung",
        }
        widgets = {
            'author': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'rating': forms.NumberInput(attrs={'class': 'input'}),
            'msg_planning': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_volunteer_event': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_construction': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_shift': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_dismantling': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_ambience': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_music': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_chief_organiser': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_catering': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_prices': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_sales': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
            'msg_misc': forms.Textarea(attrs={'class': 'textarea', 'rows': 3}),
        }
        help_texts = {
            'email': "Damit wir dich bei Rückfragen kontaktieren können.",
            'msg_shift': "Konkret zu deiner Schicht oder allgemein zum Schichtsystem.",
            'msg_chief_organiser': "Kommunikation mit den Haupt-Organisatoren (Erreichbarkeit, Freundlichkeit, "
                                   "etc.).",
            'msg_catering': "Verpflegung der Helfer",
            'rating': "Wie fandest du die Mensaparty, zusammengefasst auf eine Zahl. Werte zwischen 1 bis 10 sind "
                      "möglich, wobei 10 sehr gut und 1 sehr schlecht ist.",
        }

    def clean_rating(self):
        data = self.cleaned_data['rating']

        if data < 1:
            raise ValidationError("Die Zahl muss mind. 1 sein.")

        if data > 11:
            raise ValidationError("Sehr löblich! Leider sind nur Zahlen zwischen 1 bis 10 erlaubt.")

        return data
