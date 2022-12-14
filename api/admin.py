from django.contrib import admin
from api.models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Entry)
admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Notes)
admin.site.register(Categories)
