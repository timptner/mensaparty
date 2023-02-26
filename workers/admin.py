from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from workers.forms import UserCreationForm, WorkerForm
from workers.models import Worker


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username',),
            },
        ),
        (
            "Persönliche Informationen",
            {
                'classes': ('wide',),
                'fields': ('first_name', 'last_name', 'email'),
            },
        ),
    )

    def save_form(self, request, form, change):
        if change:
            return form.save(commit=False)
        else:
            return form.save(request, commit=True)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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
    list_display = ['last_name', 'first_name', 'is_barkeeper', 'strength', 'available_since', 'available_until']
    list_filter = ['faculty', 'is_barkeeper', StrengthListFilter]
    actions = ['contact_workers']

    @admin.action(description="Ausgewählte Helfer kontaktieren")
    def contact_workers(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        query = ','.join(str(pk) for pk in sorted(selected))
        return HttpResponseRedirect(reverse_lazy('workers:contact') + f"?workers={query}")
