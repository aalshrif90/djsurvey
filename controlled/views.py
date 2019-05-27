# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import re
#from polls.models import Question as polls_question

# This is the index.
# Validate that user must have accepted the surevy.
# If so redirecto to -pcode- views
def index(request):
    try:
        #del request.session['randomised_questions']
        del request.session['pcode']
        del request.session['justShowedProgramCode']
    except KeyError as e:
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
    # Code passed
    if "pcode" in request.session:
        return redirect('background')

    if request.method == 'POST':
        print "There is a post and code == " + request.POST["pcode"]
        pcode = request.POST["pcode"]
        if pcode:
            print "P-Code is not empty"
            if "pcode" in request.session:
                # The vistior already had a session
                # need to redirect them to their last page they stopped at ;)
                print "The vistior already had a session. The session code == " + request.session["pcode"]
                return redirect('background')
            else:
                print "There is no code session and we are creating one here."
                request.session["pcode"] = pcode
                return redirect('background')
        else:
            print "P-Code is Empty, go back to P-Code page."
            return redirect('pcode')

    return render(request, 'controlled/code.html')

# Get background Questions
def getBackgroundQuestions():
    try:
        question_cat = QuestionCategory.objects.filter(name = "background")
        if Question.objects.filter(question_category = question_cat).exists():
            return Question.objects.filter(question_category = question_cat).prefetch_related("question_dropdown")
            #for q in DropdownQuestion.objects.filter(question = question):
            #    questions.append([q, DropdownOption.objects.filter(dropdown_question = q)])
        #return questions
    except Exception as e:
        print e
        return False

# is the questions already been answered?
def isBackgroundAnswered(code):
    question_cat = QuestionCategory.objects.filter(name = "background")
    question = Question.objects.filter(question_category = question_cat)
    if Answer.objects.filter(pcode = code, question = question).exists():
        return True
    else:
        return False

# Save the background answers
def saveBackgroundAnswers(pcode, questions, answers):
    for question in questions:
        question_id = question.pk
        duration = "0"
        answer = answers.POST["question-"+str(question_id)]
        opinion_answer = u""
        #if question.opinion:
        #    opinion_answer = request.POST["question-"+str(question_id)+"-opinion"]

        answer_object = Answer(question = question,
                                pcode = pcode,
                                duration = int(duration),
                                answer = answer,
                                score = 0,
                                opinion=opinion_answer)
        answer_object.save()
        print(answer_object)
    return True

# Background request
# Then exit
def background(request):
    context = None
    pcode = None
    if "pcode" not in request.session:
        return redirect('pcode')
    else:
        pcode = request.session["pcode"]

    bg_qs = getBackgroundQuestions()
    
    if isBackgroundAnswered(pcode):
        return redirect('question')
    else:
        if request.method == 'POST':
            saveBackgroundAnswers(pcode, bg_qs, request)
            return redirect('background')
    
    return render(request, 'controlled/background.html', {'questions': bg_qs})


def showProgramCode(request):
    pcode = None
    if "pcode" not in request.session:
        return redirect('pcode')
    else:
        pcode = request.session["pcode"]

    if request.method == 'POST':
        programShowed = request.POST["programShowed"]
        duration = request.POST["time_duration"]
        programpk = request.POST["programpk"]
        # Q pk = 11
        if programShowed == u"1":
            program = Program.objects.get(pk=int(programpk))
            programOrder = ProgramOrder.objects.filter(pcode = pcode, program=program, showed = False).first()
            programOrder.showed = True
            programOrder.save()
    request.session["justShowedProgramCode"] = True
    return redirect('question')


def randomiseParticipantsToGroups(pcode):
    # Check if participant in the database
    # if not create a new one and add them to a group randomlly
    if not Participants.objects.filter(pcode = pcode).exists():
        groups = Group.objects.annotate(pcounter=Count('participants'))
        counter = 0
        prior_group_count = None
        prior_group_pk = None
        for group in groups:
            if counter == 0:
                prior_group_count = group.pcounter
                prior_group_pk = group.pk
            else:
                if group.pcounter < prior_group_count:
                    newP = Participants(group = group, pcode = pcode)
                    newP.save()
                else:
                    groupBefore = Group.objects.get(pk = prior_group_pk)
                    newP = Participants(group = groupBefore, pcode = pcode)
                    newP.save()
            counter += 1


# Getting questions program and their test suite, and test case
def getQuestions(pcode):
    returned_questions = []
    randomize = None
    participant = Participants.objects.get(pcode = pcode)
    group = Group.objects.get(pk = participant.group.pk)
    if RandomiseQuestions.objects.filter(pcode = pcode, answered = False).exists():
        q_cat = QuestionCategory.objects.get(name = "TCQ")
        questions = Question.objects.filter(question_category = q_cat, group = group).order_by('program')
        nonAnsweredQuestions = RandomiseQuestions.objects.filter(pcode = pcode, answered = False)
        for q in questions:
            if RandomiseQuestions.objects.filter(pcode = pcode, answered = False, question = q).exists():
                testCases = TestCase.objects.filter(test_suite = q.test_suite).order_by('?')
                returned_questions.append([q, q.question_text.question_text, testCases])
        return returned_questions
    #else if RandomiseQuestions.objects.filter(pcode = pcode, answered = True).exists():
    #    return returned_questions
    else:
        q_cat = QuestionCategory.objects.get(name = "TCQ")
        questions = Question.objects.filter(question_category = q_cat, group = group).order_by('program')
        for q in questions:
            testCases = TestCase.objects.filter(test_suite = q.test_suite).order_by('?')
            if not RandomiseQuestions.objects.filter(pcode = pcode, question = q).exists():
                returned_questions.append([q.pk, q.question_text.question_text, testCases])
                randomize = RandomiseQuestions(pcode = pcode, answered = False, question = q)
                randomize.save()

                # Get program order
                program = Program.objects.get(pk = q.program.pk)
                if not ProgramOrder.objects.filter(program = program, pcode = pcode).exists():
                    p_order = ProgramOrder(pcode = pcode, program = program)
                    p_order.save()
        return returned_questions

# save a test cases answers
"""
<QueryDict: {
    u'testcase-29': [u'1', u'29'], 
    u'testcase-35': [u'1', u'35'], 
    u'testcase-34': [u'1', u'34'], 
    u'testcase-33': [u'1', u'33'], 
    u'testcase-32': [u'1', u'32'], 
    u'testcase-31': [u'1', u'31'], 
    u'testcase-30': [u'1', u'30'], 
    u'questionpk': ['1'],
    u'duration': [u'10545'], 
    u'csrfmiddlewaretoken': [u'lLAPly0DVZBRQ7PuHO0KUX5Yb5sJUW67K8YzokuQVY5IrEIBvUqIyiVaEZd05ZIB']
}>
"""
def saveAnswers(pcode, answers):
    questionpk = answers["questionpk"]
    duration = answers["duration"]
    pcode = pcode
    #print "pcode = " + pcode + " questionpk = " + questionpk + " duration = " + duration
    score_counter = 0
    for answer in answers.dict():
        if "testcase-" in answer:
            testCase_id = re.sub(r'\D', "", answer)
            #print "ID = " + testCase_id
            testcase = TestCase.objects.get(pk = testCase_id)
            assertion = None
            testcase_score = 0
            #print testcase.assertion
            if testcase.assertion == 'T':
                assertion = 1
            else:
                assertion = 0
            #print assertion
            if int(answers[answer]) == assertion:
                #print "Correct add one to counter"
                score_counter += 1
                testcase_score = 1
            elif int(answers[answer]) == -1:
                testcase_score = -1
            else:
                testcase_score = 0

            # Save answered test cases
            testCaseAnswer = AnsweredTestCases(testCase = testcase, pcode = pcode, answer = answers[answer], score = testcase_score)
            testCaseAnswer.save()
    question = Question.objects.get(pk = questionpk)
    answer = Answer(question = question, pcode = pcode, duration = int(duration), score = score_counter, answer = str(answers.dict()))
    answer.save()

    # Add it was saved
    if RandomiseQuestions.objects.filter(pcode = pcode, answered = False, question = question).exists():
        rq = RandomiseQuestions.objects.get(pcode = pcode, answered = False, question = question)
        rq.answered = True
        rq.save()
    else:
        rq = RandomiseQuestions(pcode = pcode, answered = True, question = question)
        rq.save()

# Showing a Questions
def question(request):
    context = None
    pcode = None
    if "pcode" not in request.session:
        return redirect('pcode')
    else:
        pcode = request.session["pcode"]
    
    # Check if P-Code in a group or assign
    randomiseParticipantsToGroups(pcode)

    # Get Questions
    questions = []
    if "questionsList" not in request.session:
        # get program list
        questions = getQuestions(pcode)
        request.session["questionsList"] = True
    else:
        questions = getQuestions(pcode)

    print "Got Questions"
    #print questions
    if len(questions) > 0:
        print "Question size is over 0. The length is = " + str(len(questions))
        # Check to see if Program code is showed
        if "justShowedProgramCode" in request.session:
            if not request.method == 'POST':
                print "Geting the questions first in the list"
                return render(request, 'controlled/questionhalf.html', {'question': questions[0][0], 'text': questions[0][1], 'testcases': questions[0][2]})
            else:
                print "This is an answer to be saved"
                #print request.POST
                for answer in request.POST.dict():
                    print answer
                    if "testcase-" in answer:
                        matches = re.sub(r'\D', "", answer)
                        print "ID = " + matches
                saveAnswers(pcode, request.POST)
                # Remove session of showed program code
                del request.session['justShowedProgramCode']
                return redirect('question')
        else:
            if ProgramOrder.objects.filter(pcode = pcode, showed = False).exists():
                programShowed = ProgramOrder.objects.filter(pcode = pcode, showed = False).first()
                program = Program.objects.get(pk=programShowed.program.pk)
                print "Current program is the following = " + program.name
                return render(request, 'controlled/programCode.html', {'program': program})    
    else:
        return redirect('exit')

# Thank you and exit
def exit(request):
    #return HttpResponse("Hello World!")
    return render(request, 'controlled/exit.html')