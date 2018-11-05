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
assertion_types = (
    ('VPK', 'Violate PK'),
    ('VNN', 'Violate NN'),
    ('VFK', 'Violate FK'),
    ('VUQ', 'Violate UQ'),
    ('VCC', 'Violate CC'),
    ('SPK', 'Satisfy PK'),
    ('SNN', 'Satisfy NN'),
    ('SFK', 'Satisfy FK'),
    ('SUQ', 'Satisfy UQ'),
    ('SCC', 'Satisfy CC'),
)

# Technique
tech_types = (
    ('DOMINO', 'Domino'),
    ('SELECTOR', 'Selector'),
    ('SOURCER', 'Sourcer'),
    ('READER', 'Reader'),
    ('COLNAMER', 'ColumnNamer'),
    ('AVMLM', 'AVM-LM'),
    ('AVMR', 'AVM-R'),
    ('AVMD', 'AVM-D'),
)


# Models/Schema.
class Schema(models.Model):
    name = models.CharField(max_length=255, help_text = u"Name of Schema")
    body = models.TextField(help_text = u"Insert the Schema here :)")

    def __str__(self):
        return self.name

class Question(models.Model):
    schema = models.ForeignKey(Schema, help_text = u"Choose a Schema", null=True, blank=True)
    question_text = models.TextField(help_text=u"Added your Question text here.")
    question_insert_statement = models.TextField(help_text=u"If there is any insert statements, added here", null=True, blank=True)
    is_it_singlechoice = models.BooleanField(default=False, help_text=u"Is there two possiblity choice e.g. True or False?")
    is_it_multichoices = models.BooleanField(default=False, help_text=u"Is there multiple right choices ?")
    is_it_dropdown = models.BooleanField(default=False, help_text=u"Is it a dropdown?")
    is_it_opinion = models.BooleanField(default=False, help_text=u"Is it an opinion?")
    question_type = models.CharField(max_length=255, choices=question_types, default='ASSERT')
    assertion_type = models.CharField(max_length=255, choices=assertion_types, default='VPK')
    technique = models.CharField(max_length=255, choices=tech_types, null=True, blank=True)

    def __str__(self):
        return self.question_text

class Dropdown(models.Model):
    question = models.ForeignKey(Question, related_name="dropdown", help_text = u"Choose a question for this answer")
    dropdown_text = models.TextField(help_text=u"Added your Dropdown text here.")
    technique = models.CharField(max_length=255, choices=tech_types, default='DOMINO')

    def __str__(self):
        return self.dropdown_text

class Choice(models.Model):
    question = models.ForeignKey(Question, help_text = u"Choose a question for this answer")
    choice_text = models.TextField(help_text=u"Added your Choice text here.")
    right_answer = models.BooleanField(default=False, help_text=u"Is this a right answer?")
    technique = models.CharField(max_length=255, choices=tech_types, default='DOMINO')

    def __str__(self):
        return self.choice_text

class RandomisedAnswersOrder(models.Model):
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")
    question = models.ForeignKey(Question, help_text = u"List of Questins")
    timestamp = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False, help_text=u"is this question answered?")

    class Meta:
        ordering = ['timestamp']

class SchemaShowedOrder(models.Model):
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")
    schema = models.ForeignKey(Schema, help_text = u"Schema")
    timestamp = models.DateTimeField(auto_now_add=True)
    showed = models.BooleanField(default=False, help_text=u"have the schema been showed?")

    class Meta:
        ordering = ['timestamp']

class Group(models.Model):
    name = models.CharField(max_length=255, help_text = u"Name of Group")

    def __str__(self):
        return self.name

class GroupUser(models.Model):
    group = models.ForeignKey(Group)
    user_code = models.CharField(max_length=255, help_text=u"The code given to a user")

    def __str__(self):
        return "Group %s - %s" % (self.group, self.user_code)
        #return self.group + "-" + self.user_code

class GroupQuestions(models.Model):
    group = models.ForeignKey(Group)
    technique = models.CharField(max_length=255, choices=tech_types, null=True, blank=True)
    assertion_type = models.CharField(max_length=255, choices=assertion_types, default='VPK')
    schema = models.ForeignKey(Schema, help_text = u"Choose a Schema", null=True, blank=True)
    #question = models.ForeignKey(Question, help_text = u"List of Questins")

    def __str__(self):
        return "Group-%s-%s-%s-%s" % (self.group, self.technique, self.schema, self.assertion_type)
        #return self.group + "-" + self.technique + "-" + self.schema

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
        return str(self.id)
