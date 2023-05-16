from django.shortcuts import render,get_object_or_404
from django.conf import settings
from rest_framework import generics,mixins,viewsets,status
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,DetailAddtwo,DetailAdd
from .serializers import UserSerializer,RegisterSerializer,DetailAddSerializer,DetailAddTwoSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from PIL import Image
import io
import spacy
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import PyPDF2
import os

# Create your views here.   

matplotlib.use('Agg')
nlp = spacy.load('en_core_web_sm')

class BlacklistTokenView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token=request.data["refresh_token"]
            token=RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class LoggedInUserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

class RegisterView(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    serializer_class=RegisterSerializer
    queryset=User.objects.all()   

class DetailAddView(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    serializer_class=DetailAddSerializer
    queryset=DetailAdd.objects.all()  

class ResumeScannerView(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    queryset = DetailAddtwo.objects.all()
    serializer_class = DetailAddTwoSerializer
    # permission_classes=[IsAuthenticated]
    def create(self, request):
        serializer = self.serializer_class(data =request.data)
        resume_file = request.FILES.get('resume')
        file_path = default_storage.save(resume_file.name, ContentFile(resume_file.read()))
        with default_storage.open(file_path, 'rb') as pdf_file:
            pdfReader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdfReader.pages)
            text = ""
            for i in range(num_pages):
                pageObj = pdfReader.pages[i]
                text += pageObj.extract_text()
            pdf_file.close()
            text = text.replace('\n', '')
            with open(file_path+'.txt', 'w') as f:
                f.write(text)

        with open(file_path+'.txt', 'r', encoding='iso-8859-1') as f:
            text = f.read()

        text = re.sub(r'\d+', '', text)

        terms = {
            'Technical Skills': ['java', 'c', 'c++', 'python', 'django',
                                 'django rest framework', 'node.js', 'reactjs', 'vue.js',
                                 'angular', 'angularjs', 'visual studio code', 'github',
                                 'postman', 'spring boot', 'aws', 'docker', 'eclipse',
                                 'javascript', 'html', 'css'
                                ],
            'Soft Skills': ['communication', 'teamwork', 'flexibility',
                             'confidence', 'problem solving', 'self-management', 'adaptability',
                             'time management', 'empathy', 'leadership', 'creativity',
                             'project management', 'attention to detail', 'patience', 
                            ],
        }

        patterns = {
            'Technical Skills': [{'LOWER': {'IN': ['java', 'c', 'c++', 'python', 'django',
                                     'django rest framework', 'node.js', 'reactjs', 'vue.js',
                                     'angular', 'angularjs', 'visual studio code', 'github',
                                     'postman', 'spring boot', 'aws', 'docker', 'eclipse',
                                     'javascript', 'html', 'css']}}],
            'Soft Skills': [{'LOWER': {'IN': ['communication', 'teamwork', 'flexibility',
                             'confidence', 'problem solving', 'self-management', 'adaptability',
                             'time management', 'empathy', 'leadership', 'creativity',
                             'project management', 'attention to detail', 'patience']}}],
        }

        matcher = spacy.matcher.Matcher(nlp.vocab)
        for label, pattern in patterns.items():
            matcher.add(label, [pattern], on_match=None)
            
        doc = nlp(text.lower())
        matches = matcher(doc)
        list1 = []
        for match_id, start, end in matches:
            label = matcher.vocab.strings[match_id]
            span = doc[start:end]
            if span.text not in list1:
                list1.append(span.text)
                print(label, span.text)

        scores = {label: 0 for label in terms.keys()}
        for match_id, start, end in matches:
            label = matcher.vocab.strings[match_id]
            span = doc[start:end]
            if span.text in list1:
                scores[label] += 1

        summary = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
        summary.index.name = 'Category'
        summary.sort_values(by='Score', ascending=False, inplace=True)

        plt.figure(figsize=(5,5))
        plt.pie(summary['Score'], labels=summary.index, autopct='%1.0f%%', shadow=True, startangle=90)
        plt.title('Resume Decomposition by Areas')
        plt.axis('equal')

        applicant_name = resume_file.name.split('.')[0]
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        temp = f'{applicant_name}_pie_chart'
        binary_data = buf.getvalue()
        pil_img = Image.open(buf)
        image_path = os.path.join(settings.MEDIA_ROOT,'images',f'{temp}.png')
        pil_img.save(image_path)
        pil_img = Image.open(io.BytesIO(binary_data))
        pil_img.save(image_path)
        if serializer.is_valid():
            data = serializer.data
            my_model = DetailAddtwo(
                resume=data['resume'],
                mailid=data['mailid'],
                phoneno=data['phoneno'],
                linked_in_url=data['linked_in_url'],
                img=ContentFile(binary_data, name=f'{temp}.png'),
            )
        my_model.save()
        data = serializers.serialize('json', [my_model, ]) 
        return Response(data)
        
    def get(self, request):
        my_models = DetailAddtwo.objects.all()
        serializer = DetailAddTwoSerializer(my_models, many=True)
        return Response(serializer.data)


class IndResumeView(APIView):
    allowed_methods = ['GET', 'OPTIONS']
    def get(self, request, pk):
        img = get_object_or_404(DetailAddtwo, pk=pk)
        serializer = DetailAddTwoSerializer(img)
        return Response(serializer.data)
