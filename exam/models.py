from django.db import models
from api.models import User

# Create your models here.
class Topic(models.Model):
    skill=models.CharField(max_length=200)

    def __str__(self):
        return self.skill

class Question(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    question=models.CharField(max_length=200)

    def __str__(self):
        return self.question
    
class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer=models.FileField(upload_to="answer_sheet")
    options=(
            ("pending","pending"),
            ("pass","pass"),
            ("failed","failed")
            )
    status=models.CharField(max_length=200,default="pending",choices=options)

    def __str__(self):
        return self.status