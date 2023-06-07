from django.contrib import admin
from .models import Question


# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
admin.site.register(Question, QuestionAdmin)


class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "writer",
        "title"
    )
    lsit_filter =("category")