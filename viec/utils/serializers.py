from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from utils.models import City, State


class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=70, validators=[UniqueValidator(queryset=State.objects.all())])
    code = serializers.CharField(max_length=2, min_length=2, required=False)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(required=False)
    deleted_on = serializers.DateTimeField(allow_null=True, required=False)

    created_by = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, slug_field="username")
    changed_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    def create(self, validated_data):
        instance = State.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        State.objects.filter(id=instance.id).update(**validated_data)
        return State.objects.get(id=instance.id)


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=3, min_length=3, validators=[UniqueValidator(queryset=City.objects.all())])
    pin = serializers.CharField(allow_null=True, max_length=6, min_length=6, required=False)
    latitude = serializers.DecimalField(allow_null=True, decimal_places=12, max_digits=18, required=False)
    longitude = serializers.DecimalField(allow_null=True, decimal_places=12, max_digits=18, required=False)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(required=False)
    deleted_on = serializers.DateTimeField(allow_null=True, required=False)

    created_by = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, slug_field="username")
    changed_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=City.objects.all(),
                fields=('name', 'state')
            )
        ]

    def to_representation(self, instance):
        self.fields["state"] = StateSerializer(read_only=True)
        return super().to_representation(instance=instance)

    def create(self, validated_data):
        instance = City.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        City.objects.filter(id=instance.id).update(**validated_data)
        return City.objects.get(id=instance.id)
