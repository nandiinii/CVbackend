from django.shortcuts import render
from numpy import *
from rest_framework.decorators import action
from .models import InputData
from rest_framework.response import Response
from rest_framework import status,generics,mixins,viewsets
from .serializers import PersonalitySerializer
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
        gender = le.fit_transform([serializer.validated_data['gender']])[0]
        age = serializer.validated_data['age']
        Openness = serializer.validated_data['Openness']
        Conscientiousness = serializer.validated_data['Conscientiousness']
        Extraversion = serializer.validated_data['Extraversion']
        Agreeableness = serializer.validated_data['Agreeableness']
        Neuroticism = serializer.validated_data['Neuroticism']

        # Create the input vector for the model
        input_vector = [[gender, age, Openness, Neuroticism, Conscientiousness, Agreeableness, Extraversion]]

        # Load the trained model
        model=pickle.load(open('training/personality_model.pkl','rb'))

        # Make the prediction
        prediction = model.predict(input_vector)[0]
        
        if serializer.is_valid():
            data=serializer.data
            my_model = InputData(
                name=data['name'],
                gender=data['gender'],
                age=data['age'],
                Openness=data['Openness'],
                Conscientiousness=data['Conscientiousness'],
                Extraversion=data['Extraversion'],
                Agreeableness=data['Agreeableness'],
                Neuroticism = data['Neuroticism'],
                Label=prediction,
            )
        my_model.save()
        data = serializers.serialize('json', [my_model, ])
        return Response(data)
   

