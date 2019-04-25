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

admin.site.register(Program)
admin.site.register(TestSuite, TestSuiteAdmin)
admin.site.register(IndexPageContent, MarkdownxModelAdmin)