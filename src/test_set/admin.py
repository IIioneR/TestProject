from django.contrib import admin

# Register your models here.
from test_set.forms import TestForm, QuestionsInlineFormSet, AnswerInlineFormSet
from test_set.models import Question, Test, Answer


class AnswersInline(admin.TabularInline):
    model = Answer
    fields = ('text', 'is_correct')
    show_change_link = True
    extra = 0
    formset = AnswerInlineFormSet


class QuestionsAdminModel(admin.ModelAdmin):
    list_display = ('number', 'text', 'description', 'test')
    list_select_related = ('test',)
    list_per_page = 10
    search_fields = ('first_name',)
    inlines = (AnswersInline,)


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'number')  # 'num_variant_min_limit')
    show_change_link = True
    extra = 1
    formset = QuestionsInlineFormSet


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)
    form = TestForm


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionsAdminModel)
admin.site.register(Answer)
