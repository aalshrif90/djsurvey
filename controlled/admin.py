# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
#import nested_admin
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.
from .models import *

class TestCaseleInline(admin.StackedInline):
    model = TestCase
    extra = 1

class TestSuiteAdmin(admin.ModelAdmin):
    inlines = [TestCaseleInline]

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super(TestSuiteAdmin, self).get_form(request, *args, **kwargs)
        #find the user via user profile forien key
        new_id = "PROGRAM-AUTO-GENERATOR-REDUCED"
        # Initial values
        form.base_fields['test_suite_id'].initial = new_id
        return form

class ParticipantsleInline(admin.StackedInline):
    model = Participants
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [ParticipantsleInline]

class DropdownOptionInline(admin.StackedInline):
    model = DropdownOption
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [DropdownOptionInline]

"""
class QuestionCategoryleInline(admin.StackedInline):
    model = QuestionCategory
    extra = 1

class QuestionTextleInline(admin.StackedInline):
    model = QuestionText
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [QuestionCategoryleInline, QuestionTextleInline]

"""
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('pcode', 'group')

class AnswerAdmin(admin.ModelAdmin):
    def program(self, obj):
        return obj.question.program

    def id(self, obj):
        return obj.question.pk

    list_display = ('id', 'pcode', 'duration', 'score', 'program', 'timestamp', 'answer')


class AnsweredTestCasesAdmin(admin.ModelAdmin):
    def program(self, obj):
        return obj.testCase.test_suite.program

    def test_suite(self, obj):
        return obj.testCase.test_suite.other_label

    def group(self, obj):
        p = Participants.objects.get(pcode = obj.pcode)
        return p.group

    list_display = ('pk', 'pcode', 'group', 'score', 'program', 'test_suite', 'timestamp', 'answer')

class RandomiseQuestionsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pcode', 'question', 'timestamp', 'answered')

class ProgramOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pcode', 'program', 'timestamp', 'showed')

admin.site.register(Program)
admin.site.register(TestSuite, TestSuiteAdmin)
admin.site.register(IndexPageContent, MarkdownxModelAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(QuestionCategory)
admin.site.register(QuestionText)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Participants, ParticipantsAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(AnsweredTestCases, AnsweredTestCasesAdmin)
admin.site.register(RandomiseQuestions, RandomiseQuestionsAdmin)
admin.site.register(ProgramOrder, ProgramOrderAdmin)


#admin.site.register(DropdownQuestion, DropdownQuestionAdmin)