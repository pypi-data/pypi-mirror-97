import json

try:
    from django.contrib.postgres.fields import JSONField
    from django.contrib.postgres.forms.jsonb import JSONField as JSONFormField
except ImportError:
    from django.db.models import JSONField
    from django.forms import JSONField as JSONFormField

__all__ = ('UTF8JSONFormField', 'UTF8JSONField')


class UTF8JSONFormField(JSONFormField):
    def prepare_value(self, value):
        try:
            return json.dumps(value, ensure_ascii=False)
        except json.JSONDecodeError:
            return value


class UTF8JSONField(JSONField):
    """JSONField for postgres databases.

    Displays UTF-8 characters directly in the admin, i.e. äöü instead of
    unicode escape sequences.
    """

    def formfield(self, **kwargs):
        return super().formfield(**{**{'form_class': UTF8JSONFormField}, **kwargs,})
