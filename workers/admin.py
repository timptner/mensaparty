from django.contrib import admin
from workers.forms import WorkerForm
from workers.models import Worker
from django.db.models.query import EmptyQuerySet


class StrengthListFilter(admin.SimpleListFilter):
    title = "Stärke"
    parameter_name = 'strength'

    def lookups(self, request, model_admin):
        return [
            ('25', "0 bis 25 kg"),
            ('50', "26 bis 50 kg"),
            ('75', "51 bis 75 kg"),
            ('100', "76 bis 100 kg"),
        ]

    def queryset(self, request, queryset):
        if self.value() == '25':
            return queryset.filter(strength__gte=0, strength__lte=25)

        if self.value() == '50':
            return queryset.filter(strength__gt=25, strength__lte=50)

        if self.value() == '75':
            return queryset.filter(strength__gt=50, strength__lte=75)

        if self.value() == '100':
            return queryset.filter(strength__gt=75, strength__lte=100)

        if self.value():
            return Worker.objects.none()


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    form = WorkerForm
    list_display = ['__str__', 'strength']
    list_filter = ['faculty', StrengthListFilter]
