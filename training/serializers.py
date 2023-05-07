from rest_framework import serializers
from .models import InputData


class PersonalitySerializer(serializers.ModelSerializer):
         def validate(self,data):
            name=data['name']
            gender=data['gender']
            age=data['age']
            Openness=data['Openness']
            Conscientiousness=data['Conscientiousness']
            Extraversion=data['Extraversion']
            Agreeableness=data['Agreeableness']
            Neuroticism=data['Neuroticism']
            return data

         class Meta:
                model=InputData
                fields='__all__'

