from .models import *
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.
def home(response):
    if (response.user.is_authenticated):
        return render(response, 'home/user_home.html', {'name': response.user.username})
    return render(response, 'home/guest_home.html', {'name': 'user'})


def question(response, quiz_id=None, question_id=None):
    if not(quiz_id is None) and ((not response.user.is_authenticated) or (Quiz.objects.get(id=quiz_id).user != response.user)):
        return redirect('/login')
    if response.method == 'POST':
        print(quiz_id)
        qz = Quiz.objects.get(id=quiz_id) #quiz object

        picked_answer = [] #list of all selected options
        r_dict = response.POST.dict() #converts QueryDict into dict
        for i in r_dict:
            if i[0] == 'n':
                #picked_answer.append(r_dict[i])
                if (r_dict[i] == 'checked'):
                    picked_answer.append(r_dict[i])
        
        q_i = QuestionInstance.objects.get(id=question_id) #related instanced question
        result = q_i.CheckAnswerWithList(picked_answer) #check whether the answer is correct or not using the retrieved question

        next_id = qz.GetNextQuestionID(question_id) #get next question's id
        if next_id is None:
            return redirect('/')
        else:
            next_question = QuestionInstance.objects.get(id = next_id)
            return render(response, 'home/question.html', {
                'answers':next_question.GetAnswers().order_by('id'),
                'question':next_question.question_obj.question,
                'quiz_id':quiz_id,
                'question_id':next_id
                })
    if response.method == 'GET':
        get_dict = response.GET.dict()
        if '3' in get_dict:
            qz = Quiz().CreateQuiz(num = 3, usr = response.user)
            sorted_question_ids = qz.GetOrderedQuestionsAsIDs()
            q = QuestionInstance.objects.get(id=sorted_question_ids[0])

            return render(response, 'home/question.html', {
                'answers': q.GetAnswers().order_by('id'),
                'question': q.question_obj.question,
                'quiz_id': qz.id,
                'question_id': q.id
            })

        return render(response, 'home/quiz_picker.html', {})

def quiz_picker(response):
    if (not response.user.is_authenticated):
        return redirect('/')
    if response.method == 'POST':
        if '3' in response.POST.dict():
            qz = Quiz().CreateQuiz(num = 3, usr = response.user)
            sorted_question_ids = qz.GetOrderedQuestionsAsIDs()
            q = QuestionInstance.objects.get(id=sorted_question_ids[0])
            '''
            return redirect(reverse('question', kwargs={
                'answers': q.GetAnswers().order_by('id'),
                'question': q.question_obj.question,
                'quiz_id': qz.id,
                'question_id': q.id
            }))
            '''
            return redirect(
                'question/'+str(qz.id)+'/'+str(q.id),
                answers = q.GetAnswers().order_by('id'),
                question = q.question_obj.question,
                quiz_id = qz.id,
                question_id = q.id
            )
    return render(response, 'home/quiz_picker.html', {})


