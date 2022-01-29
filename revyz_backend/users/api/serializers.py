from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from ..models import Candidate, City, TechnicalSkill

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
        read_only_fields = ("id", "created_by")

    def create(self, validated_data: Any) -> City:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance: City, validated_data: Any) -> City:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().update(instance, validated_data)


class TechnicalSkillsSerializer(ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = "__all__"
        read_only_fields = ("id", "created_by")

    def create(self, validated_data: Any) -> TechnicalSkill:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance: TechnicalSkill, validated_data: Any) -> TechnicalSkill:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().update(instance, validated_data)


class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        read_only_fields = ("id", "created_by")

    def create(self, validated_data: Any) -> Candidate:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance: Candidate, validated_data: Any) -> Candidate:
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().update(instance, validated_data)
