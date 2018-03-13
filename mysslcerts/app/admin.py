from django.contrib import admin
from django import forms
from app.models import Topic, Question, Tag

admin.site.register(Tag)

class QuestionModelForm(forms.ModelForm):
    class Meta:
        fields = ['enabled', 'text', 'answer', 'sort_order', 'topic', 'tags']
        model = Question
        widgets = {
                'answer' : forms.Textarea(attrs={'rows': 30, 'cols': 100}),
        }

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'sort_order', 'answer', 'enabled', 'topic']
    list_filter  = ['topic', 'sort_order', 'enabled', 'tags']
    filter_horizontal = ['tags']
    search_fields = ['text', 'answer', 'topic__name', 'tags__word']
    form = QuestionModelForm
admin.site.register(Question, QuestionAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order', 'created', 'modified']
    list_filter  = ['created', 'modified']
    filter_horizontal = ['related_questions']
    search_fields = ['name']
admin.site.register(Topic, TopicAdmin)
