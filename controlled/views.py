# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
#from polls.models import Question as polls_question

# This is the index.
# Validate that user must have accepted the surevy.
# If so redirecto to -code- views
def index(request):
    try:
        del request.session['randomised_questions']
        del request.session['pcode']
    except KeyError:
        pass
    # Accepted or Declined
    if request.method == 'POST':
        if not 'answer' in request.POST:
            return redirect('index')
        if request.POST["answer"] == u"agree":
            return redirect('pcode')
        else:
            return redirect('https://www.google.com/')
    # If not that means it is a new visitor
    content = IndexPageContent.objects.filter(default = True).first()
    return render(request, 'controlled/index.html', {'content': content})

# Get participant code here then redirect to questions.
def pcode(request):
    # Code passed :)
    if "pcode" in request.session:
        return redirect('question')

    if request.method == 'POST':
        print "There is a post and code == " + request.POST["code"]
        code = request.POST["code"]
        if code:
            print "Code is not empty"
            if "code" in request.session:
                # The vistior already had a session
                # need to redirect them to their last page they stopped at ;)
                print "I am in code seesion checker. The session code == " + request.session["code"]
                return redirect('background')
            else:
                print "There is no code session and we are creating one here."
                request.session["code"] = code
                return redirect('background')
        else:
            print "Code is Empty"
            print "There is no code. Code is empty"
            return redirect('code')

    return render(request, 'controlled/code.html')

# Get background Questions
def get_background_questions():
    try:
        question_cat = QuestionCategory.objects.filter(name = "background")
        question = Question.objects.get(question_category = question_cat)
        questions = []
        if DropdownQuestion.objects.filter(question = question).exists():
            return DropdownQuestion.objects.filter(question = question).prefetch_related("dropdown")
            #for q in DropdownQuestion.objects.filter(question = question):
            #    questions.append([q, DropdownOption.objects.filter(dropdown_question = q)])
        #return questions
    except Exception as e:
        print e
        return False

# is the questions already been answered?
def isBackgroundAnswered(code):
    question_cat = QuestionCategory.objects.filter(name = "background")
    question = Question.objects.get(question_category = question_cat)
    if Answer.objects.filter(pcode = code, question = question).exists():
        return True
    else:
        return False

# Background request
# Then exit
def background(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]

    bg_qs = get_background_questions()

    if isBackgroundAnswered(code):
        return redirect('question')
    else:
        if request.method == 'POST':
            for question in bg_qs:
                question_id = question.question.pk
                duration = "0"
                answer = request.POST["question-"+str(question_id)]
                opinion_answer = u""
                #if question.opinion:
                #    opinion_answer = request.POST["question-"+str(question_id)+"-opinion"]

                answer_object = Answer(question = question.question,
                                        pcode = pcode,
                                        duration = int(duration),
                                        answer = answer,
                                        score = 0,
                                        opinion=opinion_answer)
                answer_object.save()

            return redirect('question')
    
    return render(request, 'controlled/background.html', {'questions': bg_qs})


def programCode(request):
    pass


def question(request):
    pass