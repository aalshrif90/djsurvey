# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# assertions
assertions = (
    ('T', 'TURE'),
    ('F', 'FALSE'),
)

# Automattion Methods
auto_meths = (
    ('MAN', 'Manual'),
    ('RND', 'Random'),
    ('AVMD', 'AVM-D'),
    ('AVMR', 'AVM-R'),
    ('DOMINOR', 'Domino-R'),
    ('DOMINOD', 'Domino-D'),
)

# Test Suite Lables
ts_label = (
    ('OR', 'Non-reduced'),
    ('RD', 'Redcued'),
)

# Index page title and content. I use it for infromation sheet and conset.
class IndexPageContent(models.Model):
    title = models.CharField(max_length=255, help_text = u"Study Title")
    text = MarkdownxField(help_text = u"Markdown Text", null=True, blank=True)
    default = models.BooleanField(default=False, help_text=u"Is this the default content?")

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def __str__(self):
        return self.title

# Program -> TestSuite -> TestCase
class Program(models.Model):
    name = models.CharField(max_length=255, help_text = u"Name of Program (e.g., Class or Schema)")
    code = models.TextField(help_text = u"Program Code", null=True, blank=True)

    def __str__(self):
        return self.name

class TestSuite(models.Model):
    test_suite_id = models.CharField(max_length=255, help_text = u"Test Suite ID")
    program = models.ForeignKey(Program, help_text = u"Choose a Program", null=False, blank=False)
    automated = models.BooleanField(default=True, help_text=u"Automated = TRUE or Manual = FALSE ? Default is TRUE")
    auto_method = models.CharField(max_length=255, choices=auto_meths, default='DOMINOR')
    other_label = models.CharField(max_length=255, choices=ts_label, default='OR')

    def __str__(self):
        return self.test_suite_id

class TestCase(models.Model):
    test_case_id = models.CharField(max_length=255, help_text = u"Test Case ID")
    test_suite = models.ForeignKey(TestSuite, help_text = u"Choose a Test Suite", null=False, blank=False)
    code = models.TextField(help_text = u"Test Case Code", null=True, blank=True)
    assertion = models.CharField(max_length=255, choices=assertions, default='T', help_text = u"""It Expects what? True or False. 
    Can be changed in models.py""")

    def __str__(self):
        return self.test_case_id


# Human Study Groups.
class Group(models.Model):
    name = models.CharField(max_length=255, help_text = u"Name of Group")

    def __str__(self):
        return self.name

class Participants(models.Model):
    group = models.ForeignKey(Group)
    pcode = models.CharField(max_length=255, help_text=u"Participant Code - Manual Generation or Automated")

    def __str__(self):
        return "Group %s - %s" % (self.group, self.pcode)

# Question Structure
class QuestionCategory(models.Model):
    name = models.TextField(help_text=u"Question Category")

    def __str__(self):
        return self.name

class QuestionText(models.Model):
    name = models.TextField(help_text=u"Unique Name for your Question")
    question_text = models.TextField(help_text=u"Question text.")

    def __str__(self):
        return self.name

class Question(models.Model):
    program = models.ForeignKey(Program, help_text = u"Choose a Program", null=True, blank=True)
    question_category = models.ForeignKey(QuestionCategory, help_text = u"Choose a Question Category", null=True, blank=True)
    question_text = models.ForeignKey(QuestionText, help_text = u"Choose a Question", null=True, blank=True)
    test_suite = models.ForeignKey(TestSuite, help_text = u"Choose a Test Suite", null=False, blank=False)
    singlechoice = models.BooleanField(default=False, help_text=u"One choice e.g. True or False?")
    multichoices = models.BooleanField(default=False, help_text=u"multiple choices?")
    opinion = models.BooleanField(default=False, help_text=u"Requiring Opinion?")

    def __str__(self):
        return self.pk

# Storing Answers
class Answer(models.Model):
    question = models.ForeignKey(Question, help_text = u"Question Answered")
    pcode = models.CharField(max_length=255, help_text=u"Participant Code")
    duration = models.BigIntegerField(help_text=u"Answering Duration (Millisconds)")
    answer = models.CharField(max_length=255, help_text=u"The answer")
    score = models.BooleanField(default=False, help_text=u"Right or Wrong")
    timestamp = models.DateTimeField(auto_now_add=True, help_text=u"Timestamp of the answer")
    opinion = models.TextField(null=True,blank=True,help_text=u"Participant Opinion")

    def __str__(self):
        return str(self.pk)

    class Meta:
            ordering = ['timestamp']


# Logging the questions showed and which participant and program --- in case of counter-balancing
class RandomisedAnswersOrder(models.Model):
    pcode = models.CharField(max_length=255, help_text=u"Participant Code")
    question = models.ForeignKey(Question, help_text = u"List of Questins")
    timestamp = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False, help_text=u"is this question answered?")

    class Meta:
        ordering = ['timestamp']

class ProgramOrder(models.Model):
    pcode = models.CharField(max_length=255, help_text=u"Participant Code")
    program = models.ForeignKey(Program, help_text = u"Schema")
    timestamp = models.DateTimeField(auto_now_add=True)
    showed = models.BooleanField(default=False, help_text=u"have the schema been showed?")

    class Meta:
        ordering = ['timestamp']