from django.shortcuts import render
from numpy import *
from rest_framework.decorators import action
from .models import InputData,Question
from rest_framework.response import Response
from rest_framework import status,generics,mixins,viewsets
from .serializers import PersonalitySerializer,AptitudeTestSerializer,QuestionSerializer
from sklearn.preprocessing import LabelEncoder
import pickle
from django.core import serializers

# Create your views here.

class PersonalityViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    queryset = InputData.objects.all()
    serializer_class = PersonalitySerializer

    def get(self, request):
        my_models = InputData.objects.all()
        serializer = PersonalitySerializer(my_models, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict_personality(self, queryset):
        serializer = PersonalitySerializer(data=queryset.data)
        serializer.is_valid(raise_exception=True)


        # Retrieve the user input data
        le = LabelEncoder()
        Gender = le.fit_transform([serializer.validated_data['Gender']])[0]
        Age = serializer.validated_data['Age']
        openness = serializer.validated_data['openness']
        neuroticism = serializer.validated_data['neuroticism']
        conscientiousness = serializer.validated_data['conscientiousness']
        agreeableness = serializer.validated_data['agreeableness']
        extraversion = serializer.validated_data['extraversion']

        # Create the input vector for the model
        input_vector = [[Gender,Age,openness,neuroticism,conscientiousness,agreeableness,extraversion]]
        # Load the trained model
        model=pickle.load(open('training/personality_model.pkl','rb'))

        # Make the prediction
        prediction = model.predict(input_vector)[0]
        
        if serializer.is_valid():
            data=serializer.data
            my_model = InputData(
                name=data['name'],
                Gender=data['Gender'],
                Age=data['Age'],
                openness=data['openness'],
                neuroticism = data['neuroticism'],
                conscientiousness=data['conscientiousness'],
                agreeableness=data['agreeableness'],
                extraversion=data['extraversion'],
                Label=prediction,
            )
        my_model.save()
        data = serializers.serialize('json', [my_model, ])
        return Response(data)
   

#Aptitude Test

class AptitudeTest(generics.CreateAPIView):
    serializer_class=QuestionSerializer
    queryset=Question.objects.all()  
    
class QuestionListView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = AptitudeTestSerializer   

    
class ScoreView(generics.GenericAPIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = AptitudeTestSerializer(questions, many=True)
        score = 0
        for data in serializer.data:
            if data['entered_answer'] == data['answer']:
                score += 1
        return Response({'score': score})