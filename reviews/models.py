from django.db import models


class Review(models.Model):
    author = models.CharField("Name", max_length=100, blank=True)
    email = models.EmailField("E-Mail-Adresse", blank=True)

    msg_planning = models.TextField("Planung", blank=True)
    msg_volunteer_event = models.TextField("Helfer-Treffen", blank=True)
    msg_construction = models.TextField("Aufbau", blank=True)
    msg_shift = models.TextField("Schicht", blank=True)
    msg_dismantling = models.TextField("Abbau", blank=True)
    msg_ambience = models.TextField("Atmosphäre", blank=True)
    msg_music = models.TextField("Musik", blank=True)
    msg_chief_organiser = models.TextField("Haupt-Organisatoren", blank=True)
    msg_catering = models.TextField("Verpflegung", blank=True)
    msg_prices = models.TextField("Preise", blank=True)
    msg_sales = models.TextField("Kartenverkauf", blank=True)
    msg_misc = models.TextField("Sonstiges", blank=True)

    rating = models.PositiveSmallIntegerField("Bewertung")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bewertung"
        verbose_name_plural = "Bewertungen"
        ordering = ['created_at']

    def __str__(self):
        return self.author or 'Anonym'
