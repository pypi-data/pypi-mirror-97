from django.conf import settings as django_settings

def settings(request):
    settings_in_templates = {}
    for attr in ["SITE_URL", "INSTANCE_DEFAULT_CLIENT", "SITE_NAME"]: # Write here the settings you want to expose to the templates.
        if (hasattr(django_settings, attr)):
            settings_in_templates[attr] = getattr(django_settings, attr)
    return {
        'settings': settings_in_templates,
    }