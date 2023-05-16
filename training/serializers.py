from rest_framework import serializers
from .models import InputData,Question


class PersonalitySerializer(serializers.ModelSerializer):
    def validate(self,data):
        name = data['name']
        Gender=data['Gender']
        Age=data['Age']
        openness=data['openness']
        neuroticism=data['neuroticism']
        conscientiousness=data['conscientiousness']
        agreeableness=data['agreeableness']
        extraversion=data['extraversion']
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