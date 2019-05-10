# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
#from polls.models import Question as polls_question

# This is the index.
# Validate that user must have accepted the surevy.
# If so redirecto to -pcode- views
def index(request):
    try:
        #del request.session['randomised_questions']
        del request.session['pcode']
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

    pass
        
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

    #print(questions)
    
    # Check to see if Program code is showed
    if ProgramOrder.objects.filter(pcode = pcode, showed = False).exists():
        programShowed = ProgramOrder.objects.filter(pcode = pcode, showed = False).first()
        program = Program.objects.get(pk=programShowed.program.pk)
        questionCounter = RandomiseQuestions.objects.filter(pcode = pcode, question__program = program, answered=False).count()
        return render(request, 'controlled/programCode.html', {'program': program, 'counter': questionCounter})

    if not request.method == 'POST':
        print questions[0]
        return render(request, 'controlled/question.html', {'question': questions[0][0], 'text': questions[0][1], 'testcases': questions[0][2]})
    else:
        print request.POST
        return redirect('question')
    """
    # if post answer save it in answers
    # if it is a question post
    if request.method == 'POST':
        question_id = request.POST["question_id"]
        duration = request.POST["time_duration"]
        answer = request.POST["answer"]
        questiontype = request.POST["question_type"]
        tech_type = request.POST["tech_type"]
        is_it_right = None
        # We need to check if question answer is right to be saved
        if is_it_right_answer(question_id, answer, questiontype):
            is_it_right = True
        else:
            is_it_right = False
        # Save the answer then go to next
        # Getting question
        q_id = int(question_id)
        q = Question.objects.get(id = q_id)
        if RandomisedAnswersOrder.objects.filter(user_code = code, question = q, answered = False).exists():
            print "The question was not answered and now we saving the new question"
            answer_object = Answer(question = q,
                                    user_code = code,
                                    time_duration = int(duration),
                                    answer = answer,
                                    is_it_right = is_it_right,
                                    question_type = questiontype,
                                    tech_type = tech_type)
            answer_object.save()
            # Need to save that question been answered
            answered_saved = answered_question(question_id, code)
            if answered_saved:
                print "Saved that the asnwer is done."
            else:
                print "ERORR: Saved that the asnwer is done."
            #question_list = getQuestions(code)
        question_list = getQuestionsOfGroup(code)

    # No more questions
    if not question_list:
        return redirect('exitQuestion')

    # paginate questions
    if len(question_list) > 0:
        paginator = Paginator(question_list, 1) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            question = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            question = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            question = paginator.page(paginator.num_pages)

        current_question = question.object_list[0]
        request.session["remainingQuestions"] = len(question_list)
        # Getting choices
        choices = get_choices(current_question.pk)
        #return HttpResponse("Hello World!")
        return render(request, 'polls/question.html', {'questions': question, 'choices': choices})
    else:
        return redirect('preference')
    """