from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import RandomQuestionSerializer, QuestionSerializer


class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        question = Question.objects.all().order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)


class AllQuestions(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
