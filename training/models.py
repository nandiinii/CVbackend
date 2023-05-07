from django.db import models

# Create your models here.

class InputData(models.Model):
    name=models.CharField(max_length=20,default="name")
    gender=models.CharField(max_length=10,default="Male")
    age = models.IntegerField()
    Openness = models.IntegerField()
    Conscientiousness = models.IntegerField()
    Extraversion = models.IntegerField()
    Agreeableness = models.IntegerField()
    Neuroticism = models.IntegerField()
    Label=models.CharField(max_length=20,default="Personality Not predicted",null=True)
    def __str__(self):
        return self.name
