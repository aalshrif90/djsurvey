# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# types
question_types = (
    ('BACKGROUND', 'Background'),
    ('ALL', 'All'),
    ('ASSERT', 'Assertion'),
    ('practice', 'Practice'),
    ('EXIT', 'Exit')
)

# types
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


# Program -> TestSuite -> TestCase
class Program(models.Model):
    name = models.CharField(max_length=255, help_text = u"Name of Program (e.g., Class or Schema)")
    code = models.TextField(help_text = u"Program Code", null=True, blank=True)

    def __str__(self):
        return self.name

class TestSuite(models.Model):
    test_suite_id = models.CharField(max_length=255, help_text = u"Test Suite ID")
    program = models.ForeignKey(Program, help_text = u"Choose a Program", null=False, blank=False)
    code = models.TextField(help_text = u"Test Suite Code", null=True, blank=True)
    automated = models.BooleanField(default=True, help_text=u"Is it a dropdown?")
    auto_method = models.CharField(max_length=255, choices=auto_meths, default='DOMINOR')

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
    pcode = models.CharField(max_length=255, help_text=u"Participants Code - Manual Generation or Automated")

    def __str__(self):
        return "Group %s - %s" % (self.group, self.pcode)
        #return self.group + "-" + self.user_code

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
    code = models.TextField(help_text=u"Code Associated with the Question", null=True, blank=True)
    is_it_singlechoice = models.BooleanField(default=False, help_text=u"One choice e.g. True or False?")
    is_it_multichoices = models.BooleanField(default=False, help_text=u"multiple choices?")
    is_it_dropdown = models.BooleanField(default=False, help_text=u"Drop Down?")
    is_it_opinion = models.BooleanField(default=False, help_text=u"Requiring Opinion?")

    def __str__(self):
        return self.pk

class Dropdown(models.Model):
    question = models.ForeignKey(Question, related_name="dropdown", help_text = u"Choose a question for this answer")
    dropdown_text = models.TextField(help_text=u"Added your Dropdown text here.")

    def __str__(self):
        return self.dropdown_text

class Choice(models.Model):
    question = models.ForeignKey(Question, help_text = u"Choose a question for this answer")
    choice_text = models.TextField(help_text=u"Added your Choice text here.")
    right_answer = models.BooleanField(default=False, help_text=u"Is this a right answer?")

    def __str__(self):
        return self.choice_text

# Storing Answers
class Answer(models.Model):
    question = models.ForeignKey(Question, help_text = u"the question answered")
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")
    time_duration = models.BigIntegerField(help_text=u"The duration time (Millisconds) to answer the question")
    answer = models.CharField(max_length=255, help_text=u"The answer. Either from a dropdown or choice")
    is_it_right = models.BooleanField(default=False, help_text=u"Did the test taker get it right?")
    question_type = models.CharField(max_length=255, help_text=u"The Question type")
    tech_type = models.CharField(max_length=255, help_text=u"Technique Type if any")
    timestamp = models.DateTimeField(auto_now_add=True, help_text=u"Timestamp of the answer")
    opinion_text = models.TextField(null=True,blank=True,help_text=u"opinion text")

    def __str__(self):
        return str(self.pk)

    class Meta:
            ordering = ['timestamp']


# Logging the questions showed and which participant and program --- in case of counter-balancing
class RandomisedAnswersOrder(models.Model):
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")
    question = models.ForeignKey(Question, help_text = u"List of Questins")
    timestamp = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False, help_text=u"is this question answered?")

    class Meta:
        ordering = ['timestamp']

class ProgramOrder(models.Model):
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")
    program = models.ForeignKey(Program, help_text = u"Schema")
    timestamp = models.DateTimeField(auto_now_add=True)
    showed = models.BooleanField(default=False, help_text=u"have the schema been showed?")

    class Meta:
        ordering = ['timestamp']