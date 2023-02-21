from django.db import models


class Worker(models.Model):
    MECHANICAL_ENGINEERING = 'MEE'
    PROCESS_AND_SYSTEMS_ENGINEERING = 'PSE'
    ELECTRICAL_ENGINEERING_AND_INFORMATION_TECHNOLOGY = 'EIT'
    COMPUTER_SCIENCE = 'COS'
    MATHEMATICS = 'MAT'
    NATURAL_SCIENCES = 'NAS'
    MEDICINE = 'MED'
    SOCIAL_SCIENCES_AND_EDUCATION = 'SSE'
    ECONOMICS_AND_MANAGEMENT = 'ECM'

    FACULTY_CHOICES = [
        (MECHANICAL_ENGINEERING, "Maschinenbau"),
        (PROCESS_AND_SYSTEMS_ENGINEERING, "Verfahrens- und Systemtechnik"),
        (ELECTRICAL_ENGINEERING_AND_INFORMATION_TECHNOLOGY, "Elektro- und Informationstechnik"),
        (COMPUTER_SCIENCE, "Informatik"),
        (MATHEMATICS, "Mathematik"),
        (NATURAL_SCIENCES, "Naturwissenschaften"),
        (MEDICINE, "Medizin"),
        (SOCIAL_SCIENCES_AND_EDUCATION, "Humanwissenschaften"),
        (ECONOMICS_AND_MANAGEMENT, "Wirtschaftswissenschaften"),
    ]

    first_name = models.CharField("Vorname", max_length=50)
    last_name = models.CharField("Nachname", max_length=50)
    email = models.EmailField("E-Mail-Adresse", unique=True)
    phone = models.CharField("Mobilnummer", max_length=20)
    faculty = models.CharField("Fakultät", max_length=3, choices=FACULTY_CHOICES)
    experience = models.TextField("Erfahrung", blank=True)
    strength = models.PositiveSmallIntegerField("Stärke")

    class Meta:
        verbose_name = "Helfer"
        verbose_name_plural = "Helfer"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
