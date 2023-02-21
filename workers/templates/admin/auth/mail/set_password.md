{% autoescape off %}Hallo {{ user.get_short_name }},

es wurde ein neuer Benutzer für dich angelegt. Bitte 
[lege ein Passwort fest]({{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}), 
damit du dich anmelden kannst.

Dein Benutzername lautet _{{ user.username }}_.

Viele Grüße  {# 2 spaces for linebreak #}
FaRaFMB{% endautoescape %}
