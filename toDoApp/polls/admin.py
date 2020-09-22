from django.contrib import admin

from .models import Question, Choice

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields' : ['questionText']}),
        ('Date Information',{'fields':['pubDate']})
        ]
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
