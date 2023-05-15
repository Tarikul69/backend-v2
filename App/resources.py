from import_export import resources
from .models import *

class StudentsResource(resources.ModelResource):
    class Meta:
        model = Students