from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QuestionInstance)
admin.site.register(Quiz)
