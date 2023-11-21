from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.CharField(max_length=255)
    element = models.CharField(max_length=1, choices=[('E','E'),('I','I'),('N', 'N'), ('S', 'S'), ('T', 'T'), ('F', 'F'), ('J', 'J'), ('P', 'P')])

class UserAnswer(models.Model):
    user_id = models.IntegerField() #임의로 id 생성 - 사용자 식별용
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
