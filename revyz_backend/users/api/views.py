import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ..models import Candidate, City, TechnicalSkill
from ..utils import aws_conn
from .serializers import (
    CandidateSerializer,
    CitySerializer,
    TechnicalSkillsSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CityViewSet(ModelViewSet):

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter]
    search_fields = ["city_name"]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TechnicalSkillsViewSet(ModelViewSet):

    queryset = TechnicalSkill.objects.all()
    serializer_class = TechnicalSkillsSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter]
    search_fields = ["skill_name"]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CandidateViewSet(ModelViewSet):

    queryset = (
        Candidate.objects.prefetch_related("tech_skills")
        .select_related("city_id")
        .all()
    )
    serializer_class = CandidateSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [SearchFilter]
    search_fields = ["name", "email", "city_id__city_name", "tech_skills__skill_name"]

    def create(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_name="pushtosqs")
    def SendRecordSQS(self, request, pk=None):
        sqs_client = aws_conn("sqs", "ap-south-1")

        country_obj = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(country_obj)

        message = {"key": serializer.data}
        response = sqs_client.send_message(
            QueueUrl="https://ap-south-1.queue.amazonaws.com/084914436259/test_queue_service",
            MessageBody=json.dumps(message),
        )

        return Response(response)
