from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import authentication, permissions
from rest_framework import generics

from exam.serializers import TopicSerializer,QuestionSerializer,AnswerSerializer
from exam.models import Topic,Question,Answer

# Create your views here.


class TopicAddView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

    serializer_class=TopicSerializer
    queryset=Topic.objects.all()

class AddQuestionView(generics.CreateAPIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

    queryset =Question.objects.all()
    serializer_class =QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class ViewQuestionView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]

    queryset =Question.objects.all()
    serializer_class =QuestionSerializer

class TopicQuestionsView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        # Retrieve the topic_id from the URL parameter
        topic_id = self.kwargs.get('topic_id')
        
        # Get the Topic instance based on the topic_id
        topic = get_object_or_404(Topic, id=topic_id)

        # Retrieve and return the questions for the specified topic
        return Question.objects.filter(topic=topic)
    
class AnswerAddView(viewsets.ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=AnswerSerializer
    queryset=Answer.objects.all()

    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("Permission Deneid")
    
    def perform_create(self, serializer):
        # Access the user ID from the Token
        serializer.save(user=self.request.user)

def download_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    authentication.TokenAuthentication
    permissions.IsAdminUser
    
    # Assuming 'answer' is the FileField in your model
    with open(answer.answer.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={answer.answer.name}'
        return response