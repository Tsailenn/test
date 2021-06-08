from django.test import TestCase
from . import models
from django.contrib.auth.models import User

# Create your tests here.
class QuizCreationTestCase(TestCase):
    def SetUp(self):
        u = User.objects.create(
            username='deez',
            password='nuts'
        )
        q = models.Question.objects.create(
            question='Do you know who is Dwight?'
            )
        a1 = models.Answer.objects.create(
            answer = 'no',
            correct = False,
            question_obj=q
        )
        a2 = models.Answer.objects.create(
            answer = 'D-WIGHT STUFF ON YOUR MOUTH LLLLLLLLLLLLL',
            correct = True,
            question_obj=q
        )
        qz = models.Quiz.objects.create(
            user = u
        )
        q_i = models.QuestionInstance.objects.create(
            answered_correct=False,
            question_obj = q,
            quiz_obj = qz
        )
        print(qz.CalculateScore())
    
    def GenerateQuestion1(self):
        q = models.Question.objects.create(
            question = '125'
        )
        a1 = models.Answer.objects.create(
            answer='1',
            correct = True,
            question_obj = q
        )
        a2 = models.Answer.objects.create(
            answer ='2',
            correct = True,
            question_obj = q
        )
        a3 = models.Answer.objects.create(
            answer = '3',
            correct = False,
            question_obj = q
        )
        a4 = models.Answer.objects.create(
            answer = '4',
            correct = False,
            question_obj = q
        )
        a5 = models.Answer.objects.create(
            answer = '5',
            correct = True,
            question_obj = q
        )
        return q

    def GenerateQuestion2(self):
        q = models.Question.objects.create(
            question = '23'
        )
        a1 = models.Answer.objects.create(
            answer='1',
            correct = False,
            question_obj = q
        )
        a2 = models.Answer.objects.create(
            answer ='2',
            correct = True,
            question_obj = q
        )
        a3 = models.Answer.objects.create(
            answer = '3',
            correct = True,
            question_obj = q
        )
        a4 = models.Answer.objects.create(
            answer = '4',
            correct = False,
            question_obj = q
        )
        return q

    def GenerateQuestion3(self):
        q = models.Question.objects.create(
            question = '2345'
        )
        a1 = models.Answer.objects.create(
            answer='1',
            correct = False,
            question_obj = q
        )
        a2 = models.Answer.objects.create(
            answer ='2',
            correct = True,
            question_obj = q
        )
        a3 = models.Answer.objects.create(
            answer = '3',
            correct = True,
            question_obj = q
        )
        a4 = models.Answer.objects.create(
            answer = '4',
            correct = True,
            question_obj = q
        )
        a5 = models.Answer.objects.create(
            answer = '5',
            correct = True,
            question_obj = q
        )
        return q

    def GenerateQuestion4(self):
        q = models.Question.objects.create(
            question = '1'
        )
        a1 = models.Answer.objects.create(
            answer='1',
            correct = True,
            question_obj = q
        )
        a2 = models.Answer.objects.create(
            answer ='2',
            correct = False,
            question_obj = q
        )
        return q

    def GenerateUser(self):
        u = User.objects.create(
            username = 'amogus',
            password = 'sus'
        )
        return u

    def GenerateQuiz(self, num, usr):
        qz = models.Quiz().CreateQuiz(num=num, usr=usr)
        return qz
    
    def QuizGenerationTest(self):
        u = self.GenerateUser()
        self.GenerateQuestion1()
        self.GenerateQuestion2()
        self.GenerateQuestion3()
        self.GenerateQuestion4()
        qz = self.GenerateQuiz(3, u)
        print(qz)
        for i in qz.instances.all():
            print(i.question_obj.question)
        for i in qz.instances.all():
            print(i.GetCorrectAnswers())

    '''
    def DataValidation(self):
        self.SetUp();
        question_pool = models.Question.objects.all()
        q = models.Question.objects.first()
        print(question_pool)
        print(q)
        print(type(q))
        print(q.GetCorrectAnswers())
        c_answer = q.GetCorrectAnswers()
        w_answer = q.GetAnswers().filter(correct=False)
        q_inst = models.QuestionInstance.objects.first()
        print(c_answer)
        print(q_inst)
        print(q_inst.CheckAnswer(c_answer))
        print(w_answer)
        print(q_inst.CheckAnswer(w_answer))
    '''