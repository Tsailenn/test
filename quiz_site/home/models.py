from django.db import models
from django.contrib.auth.models import User
import numpy as np
from numpy.core.numeric import NaN

class Question(models.Model):
    question = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.question
    
    def GetAnswers(self):
        related_answers = self.answers.all()
        return related_answers
    
    def GetCorrectAnswers(self):
        correct_answers = self.answers.filter(correct=True)
        return correct_answers

class Answer(models.Model):
    answer = models.CharField(max_length=1024)
    correct = models.BooleanField(default=False)
    question_obj = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.answer

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizes')

    def CalculateScore(self):
        related_questions = self.instances.all()
        correct_questions = related_questions.filter(answered_correct=True)
        return (len(correct_questions) / len(related_questions)) * 100
    
    def CreateQuiz(self, num, usr):
        question_id_pool = list(Question.objects.values_list('id', flat=True))
        selected_id = []
        qz = Quiz.objects.create(
            user = usr
        )
        if (num > len(question_id_pool)):
            num = len(question_id_pool)
        selected_id = np.random.choice(question_id_pool, num, replace=False)
        for i in Question.objects.filter(id__in=selected_id):
            QuestionInstance.objects.create(
                answered_correct = False,
                question_obj = i,
                quiz_obj = qz
            )
        return qz
    
    def GetOrderedQuestionsAsIDs(self):
        q = self.instances.all().order_by('id')
        ids = list(q.values_list('id', flat=True))
        return ids
    
    def GetNextQuestionID(self, current_id):
        ids = self.GetOrderedQuestionsAsIDs()
        if current_id == ids[-1]:
            return None
        else:
            ind = ids.index(current_id) + 1
            return ids[ind]


class QuestionInstance(models.Model):
    answered_correct = models.BooleanField(default=False)
    question_obj = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='dupe')
    quiz_obj = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='instances')

    def GetAnswers(self):
        return self.question_obj.GetAnswers()
    
    def GetCorrectAnswers(self):
        return self.question_obj.GetCorrectAnswers()

    def CheckAnswerWithQuerySet(self, q):
        correct_pool = self.GetCorrectAnswers()
        correct = False
        if (len(q) == len(correct_pool)):
            for i in q: 
                if (i in correct_pool):
                    correct = True
                else:
                    correct = False
                    break
            self.answered_correct = correct
            self.save()
            return self.answered_correct
        else:
            return False

    def CheckAnswerWithList(self, a): #list(Question.objects.values_list('id', flat=True))
        correct_pool = list(self.GetCorrectAnswers().values_list('id', flat=True))
        correct = False
        if (len(correct_pool != a)):
            self.answered_correct = False
            self.save()
            return False
        else:
            for i in a:
                if (i in correct_pool):
                    correct = True
                else:
                    correct = False
                    break
            self.answered_correct = correct
            self.save()
            return correct



