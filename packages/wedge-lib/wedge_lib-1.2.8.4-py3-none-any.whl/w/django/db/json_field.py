import json

from django.db import models


# noinspection PyMethodMayBeStatic
class JsonField(models.TextField):
    def from_db_value(self, value, expression, connection):
        """ convert string from db to python dictionary """
        if value is None:
            return None
        return json.loads(value)

    def to_python(self, value):
        """ convert model input value to python dictionary """
        return None if value is None else json.dumps(value)
