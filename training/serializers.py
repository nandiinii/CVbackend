from rest_framework import serializers
from .models import InputData,Question


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    
class AptitudeTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4','entered_answer','answer']