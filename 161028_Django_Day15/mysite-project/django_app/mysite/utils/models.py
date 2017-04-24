from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def url_field(self, fieldname, default=''):
        field = getattr(self, fieldname)
        if field and hasattr(field, 'url'):
            return field.url
        return default
