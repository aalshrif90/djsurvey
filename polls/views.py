# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import timedelta

# Importing models
from .models import *

"""
Notes:
- I must use session to track question answered
- Need to implement timer and pass it through the form
"""

# This is the index.
# Validate that user must have accepted the surevy.
# If so redirecto to -code- views
def index(request):
    #return HttpResponse("Hello World!")
    """
    if "code" in request.session:
        return redirect('question')
    """
    try:
        del request.session['totalQuestions']
        del request.session['questions_poulated']
        del request.session['code']
    except KeyError:
        pass
    # Accepted or Declined
    if request.method == 'POST':
        if not 'answer' in request.POST:
            return redirect('index')
        if request.POST["answer"] == u"agree":
            return redirect('code')
        else:
            return redirect('https://www.google.com/')
    #add_i_donot_know()
    #add_info_to_q()
    # If not that means it is a new visitor
    return render(request, 'polls/index.html')

# I should get user code here then redirect to questions.
def code(request):
    # Code passed :)
    if "code" in request.session:
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

    return render(request, 'polls/code.html')


# Questions (must be random) then paginate on each question.
# Randomise(Schemas) -get-> questions sequence.
# Send user to each question.
# When done got to background.
def question(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]
    randomisedUsersToGroups(code)
    # List of answered questions by code
    question_list = []
    #answered_questions = []
    """
    try:
        del request.session['questions_poulated']
        #del request.session['questions']
    except KeyError:
        pass
    """
    # get schemas and Randomise
    if "questions_poulated" not in request.session:
        # get questions list
        #question_list = getQuestions(code)
        question_list = getQuestionsOfGroup(code)
        question_list = getQuestionsOfGroup(code)
        try:
            del request.session['totalQuestions']
        except KeyError:
            pass
        for q in question_list:
            print "Q id == " + str(q.pk)
        request.session["totalQuestions"] = len(question_list)
        request.session["questions_poulated"] = True
    else:
        #question_list = getQuestions(code)
        question_list = getQuestionsOfGroup(code)

    print len(question_list)
    # Number of Questions left
    # No more questions
    if not question_list:
        return redirect('exit')

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

    # Show the schema if not showed before
    if SchemaShowedOrder.objects.filter(user_code = code, schema=question_list[0].schema ,showed = False).exists():
        schemaShowedorder = SchemaShowedOrder.objects.filter(user_code = code, schema=question_list[0].schema ,showed = False).first()
        schema = Schema.objects.get(pk=schemaShowedorder.schema.pk)
        questionCounter = RandomisedAnswersOrder.objects.filter(user_code=code, question__schema=schema, answered=False).count()
        #schemaShowedorder.showed = True
        #schemaShowedorder.save()
        return render(request, 'polls/schema.html', {'schema': schema, 'counter': questionCounter})

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

# Schema Have bees showed and timed
def schemaShowed(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]
    print("HI")

    if request.method == 'POST':
        showedSchema = request.POST["schemaShowed"]
        duration = request.POST["time_duration"]
        schemapk = request.POST["schemapk"]
        # Q pk = 11
        if showedSchema == u"1":
            # Not dynamic
            q = Question.objects.get(id = 11)
            answer_object = Answer(question = q,
                                    user_code = code,
                                    time_duration = int(duration),
                                    answer = showedSchema,
                                    is_it_right = True,
                                    question_type = u"showedSchema",
                                    tech_type = u"showedSchema")
            answer_object.save()
            schema = Schema.objects.get(pk=int(schemapk))

            schemaShowedorder = SchemaShowedOrder.objects.filter(user_code = code, schema=schema ,showed = False).first()
            schemaShowedorder.showed = True
            schemaShowedorder.save()
    return redirect('question')

# Background request
# Then exit
def background(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]

    bg_qs = get_bg_questions()

    if isBackgroundAnswered(code):
        return redirect('question')
    else:
        if request.method == 'POST':
            for question in bg_qs:
                question_id = question.pk
                duration = "0"
                questiontype = "BACKGROUND"
                tech_type = "NONE"
                answer = request.POST["question-"+str(question_id)]
                opinion_answer = u""
                if question.is_it_opinion:
                    opinion_answer = request.POST["question-"+str(question_id)+"-opinion"]
                is_it_right = True

                answer_object = Answer(question = question,
                                        user_code = code,
                                        time_duration = int(duration),
                                        answer = answer,
                                        is_it_right = is_it_right,
                                        question_type = questiontype,
                                        tech_type = tech_type,
                                        opinion_text=opinion_answer)
                answer_object.save()
            return redirect('question')

    return render(request, 'polls/background.html', {'questions': bg_qs})
    #return HttpResponse("Hello World!")

def prefernceQuetion(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]

    are_all_questions_answered = returnRandomisedQuestionsThatNotBeenAnswered(code)

    # Need all questions to be answered first
    if len(are_all_questions_answered) > 0:
        return redirect('question')

    if isPreferanceAnswered(code):
        return redirect('exit')
    else:
        if request.method == 'POST':
            question_id = request.POST["question_id"]
            duration = "0"
            questiontype = request.POST["question_type"]
            tech_type = request.POST["answer"]
            answer = request.POST["answer"]
            is_it_right = True

            question = Question.objects.get(pk = int(question_id))
            answer_object = Answer(question = question,
                                    user_code = code,
                                    time_duration = int(duration),
                                    answer = answer,
                                    is_it_right = is_it_right,
                                    question_type = questiontype,
                                    tech_type = answer)
            answer_object.save()
            return redirect('exit')

    # Getting preference Question and adding it at the end of questions
    question = getPreferanceQuestions()[0]
    """
    preferQues = getPreferanceQuestions()
    for q in preferQues:
        questions.append(q)
    """
    choices = get_choices(question.pk)

    return render(request, 'polls/preference.html', {'question': question, 'choices': choices})


def exitQuestion(request):
    context = None
    code = None
    if "code" not in request.session:
        return redirect('code')
    else:
        code = request.session["code"]

    are_all_questions_answered = returnRandomisedQuestionsThatNotBeenAnswered(code)

    # Need all questions to be answered first
    if len(are_all_questions_answered) > 0:
        return redirect('question')

    questions = getExitQuestions()

    if isExitAnswered(code):
        return redirect('exit')
    else:
        if request.method == 'POST':
            for question in questions:
                question_id = question.pk
                duration = "0"
                questiontype = "EXIT"
                tech_type = "NONE"
                answer = u"Check Opinon answer column"
                opinion_answer = request.POST["question-"+str(question_id)+"-opinion"]
                is_it_right = True

                answer_object = Answer(question = question,
                                        user_code = code,
                                        time_duration = int(duration),
                                        answer = answer,
                                        is_it_right = is_it_right,
                                        question_type = questiontype,
                                        tech_type = tech_type,
                                        opinion_text=opinion_answer)
                answer_object.save()
            return redirect('exit')

    # Getting exit Question and adding it at the end of questions
    """
    preferQues = getPreferanceQuestions()
    for q in preferQues:
        questions.append(q)
    """
    #choices = get_choices(question.pk)

    return render(request, 'polls/exitQuestion.html', {'questions': questions})


def randomisedUsersToGroups(code):
    if GroupUser.objects.filter(user_code = code).exists():
        pass
    else:
        # Get all groups
        groups = Group.objects.order_by('pk').all()
        # What if the GroupUser table is empty
        counter = 0
        done = False
        for i in range(len(groups)):
            if not done:
                counter = counter + 1
                current_group_counter = None
                next_group_counter = None
                if GroupUser.objects.filter(group=groups[i]).exists():
                    current_group_counter = GroupUser.objects.filter(group=groups[i]).count()
                else:
                    new_groupuser = GroupUser(group = Group.objects.get(pk = groups[i].pk), user_code = code)
                    new_groupuser.save()
                    done = True
                if not done:
                    if counter >= len(groups):
                        new_groupuser = GroupUser(group = Group.objects.get(pk = groups[0].pk), user_code = code)
                        new_groupuser.save()
                        done = True
                    else:
                        if GroupUser.objects.filter(group=groups[counter]).exists():
                            next_group_counter = GroupUser.objects.filter(group=groups[counter]).count()
                        else:
                            new_groupuser = GroupUser(group = Group.objects.get(pk = groups[counter].pk), user_code = code)
                            new_groupuser.save()
                            done = True
                if not done:
                    if current_group_counter > next_group_counter:
                        new_groupuser = GroupUser(group = Group.objects.get(pk = groups[counter].pk), user_code = code)
                        new_groupuser.save()
                        done = True
                    elif current_group_counter < next_group_counter:
                        new_groupuser = GroupUser(group = Group.objects.get(pk = groups[i].pk), user_code = code)
                        new_groupuser.save()
                        done = True


# Thank you and exit
def exit(request):
    #return HttpResponse("Hello World!")
    return render(request, 'polls/exit.html')


def checkIfUserHasBeenRandomised(code):
    answers_objects = RandomisedAnswersOrder.objects.filter(user_code = code).all()
    if answers_objects.exists():
        return True
    else:
        return False

def returnRandomisedQuestionsThatNotBeenAnswered(code):
    randomisedQuestions = RandomisedAnswersOrder.objects.filter(user_code = code, answered = False)
    randomisedQs = []
    for ordered in randomisedQuestions:
        q = Question.objects.get(pk=ordered.question.pk)
        randomisedQs.append(q)

    return randomisedQs

def returnNotShowedSchemas(code):
    randomisedSchemas = SchemaShowedOrder.objects.filter(user_code = code, showed = False)
    randomisedSs = []
    for ordered in randomisedSchemas:
        randomisedSs.append(ordered)

    return randomisedSs

def getPreferanceQuestions():
    questions = Question.objects.filter(question_type = "ALL")
    randomisedQs = []
    for ordered in questions:
        randomisedQs.append(ordered)

    return randomisedQs


def getExitQuestions():
    questions = Question.objects.filter(question_type = "EXIT")
    randomisedQs = []
    for ordered in questions:
        randomisedQs.append(ordered)

    return randomisedQs

# Get randomised questions :)
def getQuestions(code):
    # Check user answered or not
    # IF answered remove from the list :)
    # Randomise
    questions = {}
    randomisedQs = []
    randomisedSchema = []
    # Question Dic
    if not checkIfUserHasBeenRandomised(code):
        schemas = Schema.objects.order_by('?')
        for schema in schemas:
            # If there is questions already answered
            # Randomise questions
            questions[schema] = Question.objects.select_related().filter(schema = schema, question_type = "ASSERT").order_by('?')
            randomisedSchema.append(schema)
            for q in questions[schema]:
                randomisedQs.append(q)
        for q in randomisedQs:
            if not RandomisedAnswersOrder.objects.filter(user_code=code, question=q).exists():
                b = RandomisedAnswersOrder(user_code=code, question=q)
                b.save()
        for s in randomisedSchema:
            if not SchemaShowedOrder.objects.filter(user_code=code, schema=s).exists():
                b = SchemaShowedOrder(user_code=code, schema=s)
                b.save()
    else:
        randomisedQs = returnRandomisedQuestionsThatNotBeenAnswered(code)

    return randomisedQs

# Get group questions :)
def getQuestionsOfGroup(code):
    # Check user answered or not
    # IF answered remove from the list :)
    # Randomise
    questions = {}
    randomisedQs = []
    randomisedSchema = []
    # Question Dic
    if not checkIfUserHasBeenRandomised(code):
        # Get User Group
        groupUser = GroupUser.objects.get(user_code=code)
        # Get Schemas for groups distinct
        group_schemas = list(GroupQuestions.objects.values('schema').distinct())
        # Randomise Schemas
        import random
        random.shuffle(group_schemas)
        # loop through each schema
        for s in group_schemas:
            # Get the group and its questions for current schema
            grp_qs = GroupQuestions.objects.filter(group = groupUser.group, schema__pk = s['schema']).order_by('?')
            # Add questions
            # Loop in each question assigned to this group and schema
            for grp_q in grp_qs.iterator():
                # Get the technique
                technique = grp_q.technique
                # Get the assertion type
                assertion_type = grp_q.assertion_type
                # In questions dict add the schema, then get all questions for that schema, technique, assertion randomally
                qs = Question.objects.filter(schema__pk = s['schema'], question_type = "ASSERT", technique = technique, assertion_type = assertion_type).order_by('?')
                #questions[s['schema']] = qs
                # Add main questions into a list
                #for q in questions[s['schema']]:
                for q in qs.iterator():
                    randomisedQs.insert(0, q)
                # Add practice questions at the beginning
                qs = Question.objects.filter(schema__pk = s['schema'], question_type = "practice").order_by('?')
                #questions[s['schema']] = qs
                for q in qs.iterator():
                    randomisedQs.insert(0, q)

                # This is for randimised schema
                randomisedSchema.append(s['schema'])
        for q in randomisedQs:
            if not RandomisedAnswersOrder.objects.filter(user_code=code, question=q).exists():
                b = RandomisedAnswersOrder(user_code=code, question=q)
                b.save()

        for s in randomisedSchema:
            if not SchemaShowedOrder.objects.filter(user_code=code, schema__pk=s).exists():
                schema = Schema.objects.get(pk = s)
                b = SchemaShowedOrder(user_code=code, schema=schema)
                b.save()
    else:
        randomisedQs = returnRandomisedQuestionsThatNotBeenAnswered(code)
    return randomisedQs

# is exit Question Answered
def isExitAnswered(code):
    if Answer.objects.filter(user_code = code, question_type = "EXIT").exists():
        return True
    else:
        return False

def isBackgroundAnswered(code):
    if Answer.objects.filter(user_code = code, question_type = "BACKGROUND").exists():
        return True
    else:
        return False

# is Preferance Question Answered
def isPreferanceAnswered(code):
    if Answer.objects.filter(user_code = code, question_type = "ALL").exists():
        return True
    else:
        return False
# Question been answered
def answered_question(question_id, code):
    try:
        questionanswred = RandomisedAnswersOrder.objects.get(user_code = code, question = question_id)
        questionanswred.answered = True
        questionanswred.save()
        return True
    except Exception as e:
        print e
        return False

# Get choics for the question
def get_choices(question_id):
    try:
        choices = Choice.objects.filter(question = question_id)
        return choices
    except Exception as e:
        print e

# Question been answered
def is_it_right_answer(question_id, answer, question_type):
    try:
        question = Question.objects.get(pk = question_id)
        if question_type == "ASSERT":
            choice = Choice.objects.get(question__pk = question_id, choice_text = answer)
            if choice.right_answer:
                return True
            else:
                return False
    except Exception as e:
        print e
        return False

# Get background Questions
def get_bg_questions():
    try:
        bk_questions = Question.objects.select_related().filter(question_type = "BACKGROUND")
        return bk_questions
    except Exception as e:
        print e
        return False


def add_i_donot_know():
    try:
        questions = Question.objects.filter(question_type = "ASSERT")
        for q in questions:
            choice = Choice(question = q,
                            choice_text = u"I do not know",
                            right_answer = False,
                            technique = q.technique)
            choice.save()
            print(choice)
        return True
    except Exception as e:
        print e
        return False

def add_info_to_q():
    try:
        questions = Question.objects.filter(question_type = "ASSERT")
        for q in questions:
            qtext = u"Which of the following statements will be rejected by the database? (Assume that the following INSERT statements are sequential)"
            q.question_text = qtext
            q.save()
            print(q)
        return True
    except Exception as e:
        print e
        return False


def printAllQuestions(request):
    randomisedQs = []
    grp_qs = GroupQuestions.objects.all().order_by('group')
    # Add questions
    # loop through each schema
    for grp_q in grp_qs:
        # Get the technique
        technique = grp_q.technique
        # Get the assertion type
        assertion_type = grp_q.assertion_type
        # Get schema
        schema = grp_q.schema
        # In questions dict add the schema, then get all questions for that schema, technique, assertion randomally
        qs = Question.objects.filter(schema = schema, question_type = "ASSERT", technique = technique, assertion_type = assertion_type)
        #questions[s['schema']] = qs
        # Add main questions into a list
        #for q in questions[s['schema']]:
        for q in qs:
            randomisedQs.insert(0, q)

    return render(request, 'polls/printquestions.html', {'randomisedQs': randomisedQs})
