# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import nested_admin

# Register your models here.
from .models import *

class DropdownInline(admin.StackedInline):
    model = Dropdown
    extra = 1
    #sortable_field_name = "position"

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1
    #sortable_field_name = "position"

class QuestionAdmin(admin.ModelAdmin):
    def answers(self, obj):
        the_right_answer = Choice.objects.filter(question = obj.pk)
        answer = ",".join(str(a.choice_text) for a in the_right_answer)
        return answer

    def right_answer(self, obj):
        the_right_answer = Choice.objects.filter(question = obj.pk, right_answer = True)
        answer = ",".join(str(a.choice_text) for a in the_right_answer)
        return answer

    list_display = ('question_text', 'is_it_singlechoice', 'is_it_dropdown', 'schema', 'technique', 'assertion_type', 'question_type', 'answers', 'right_answer')
    inlines = [DropdownInline, ChoiceInline]
"""
class SchemaAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
"""

class ChoiceAdmin(admin.ModelAdmin):
    def get_schema(self, obj):
        return obj.question.schema

    def get_assertion(self, obj):
        return obj.question.assertion_type

    def get_type(self, obj):
        return obj.question.question_type

    def get_technique(self, obj):
        return obj.question.technique
    list_display = ('question', 'choice_text', 'right_answer', 'get_schema', 'get_assertion', 'get_type', 'get_technique')

class DropdownAdmin(admin.ModelAdmin):
    def get_schema(self, obj):
        return obj.question.schema

    def get_assertion(self, obj):
        return obj.question.assertion_type

    def get_type(self, obj):
        return obj.question.question_type

    def get_technique(self, obj):
        return obj.question.technique
    list_display = ('question', 'dropdown_text', 'get_schema', 'get_assertion', 'get_type', 'get_technique')

class AnswerAdmin(admin.ModelAdmin):
    def get_schema(self, obj):
        return obj.question.schema

    def question_id(self, obj):
        return obj.question.pk

    def get_assertion(self, obj):
        return obj.question.assertion_type

    list_display = ('question_id', 'user_code', 'time_duration', 'answer', 'is_it_right', 'question_type', 'tech_type', 'get_assertion','get_schema','timestamp')

class RandomisedAnswersOrderAdmin(admin.ModelAdmin):
    def get_schema(self, obj):
        return obj.question.schema

    def get_assertion(self, obj):
        return obj.question.assertion_type

    def get_question_id(self, obj):
        return obj.question.pk

    def get_type(self, obj):
        return obj.question.question_type

    def get_technique(self, obj):
        return obj.question.technique

    list_display = ('user_code', 'answered', 'get_question_id', 'get_schema', 'get_type', 'get_assertion', 'get_technique')

class SchemaShowedOrderAdmin(admin.ModelAdmin):
    list_display = ('user_code', 'schema', 'showed')

admin.site.register(Schema)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(RandomisedAnswersOrder, RandomisedAnswersOrderAdmin)
admin.site.register(SchemaShowedOrder, SchemaShowedOrderAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Dropdown, DropdownAdmin)
admin.site.register(Group)
admin.site.register(GroupQuestions)
admin.site.register(GroupUser)
