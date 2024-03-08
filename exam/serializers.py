from django.contrib.auth.models import User
from rest_framework import serializers
from exam.models import Topic,Question,Answer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic
        fields="__all__"
        read_only_fields=["id",]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields="__all__"
        read_only_fields=["id"]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields="__all__"
        read_only_fields=["user",
                          "status",
                          ]