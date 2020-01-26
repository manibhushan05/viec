from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.helper import get_or_none
from employee.models import Profile
from utils.validators import validate_mobile_number, validate_pin, validate_username


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=80, validators=[UniqueValidator(queryset=Group.objects.all())])
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)

    def to_representation(self, instance):
        self.fields['permissions'] = PermissionSerializer(many=True, read_only=True)
        return super().to_representation(instance=instance)

    def create(self, validated_data):
        permissions = []
        if "permissions" in validated_data.keys():
            permissions = validated_data.pop('permissions')
        instance = Group.objects.create(**validated_data)

        for permission in permissions:
            instance.permissions.add(permission)

    def update(self, instance, validated_data):
        permissions = []
        instance = Group.objects.filter(id=instance.id)
        if "permissions" in validated_data.keys():
            instance.permission.clear()
            permissions = validated_data.pop('permissions')
        instance = instance.update(**validated_data)
        for permission in permissions:
            instance.permissions.add(permission)
        # instance.save()
        return instance


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(allow_null=True, min_length=3, max_length=200)
    contact_person_name = serializers.CharField(allow_null=True, max_length=70, required=False)
    contact_person_phone = serializers.CharField(allow_null=True, max_length=10, required=False)
    phone = serializers.CharField(allow_null=True, max_length=10, required=False)
    alternate_phone = serializers.CharField(allow_null=True, max_length=10, required=False)
    email = serializers.EmailField(allow_null=True, max_length=100, required=False)
    alternate_email = serializers.EmailField(allow_null=True, max_length=100, required=False)
    address = serializers.CharField(allow_null=True, min_length=3, max_length=300, required=False)
    pin = serializers.CharField(allow_null=True, max_length=6, min_length=6, required=False)
    designation = serializers.CharField(allow_null=True, min_length=3, max_length=100, required=False)
    organization = serializers.CharField(allow_null=True, max_length=100, required=False)
    comment = serializers.CharField(allow_null=True, required=False, max_length=500)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    deleted = serializers.BooleanField(required=False)
    deleted_on = serializers.DateTimeField(allow_null=True, required=False)

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              validators=[UniqueValidator(queryset=Profile.objects.all())])
    city = serializers.CharField(allow_null=True, min_length=3, max_length=100, required=False)

    def validate_phone(self, value):
        if not validate_mobile_number(value) and value:
            raise serializers.ValidationError("Not a valid mobile number")
        return value

    def validate_alternate_phone(self, value):
        if not validate_mobile_number(value) and value:
            raise serializers.ValidationError("Not a valid mobile number")
        return value

    def validate_contact_person_phone(self, value):
        if not validate_mobile_number(value) and value:
            raise serializers.ValidationError("Not a valid mobile number")
        return value

    def validate_pin(self, value):
        if not validate_pin(value) and value:
            raise serializers.ValidationError("Not a valid PIN")
        return value

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super().to_representation(instance=instance)

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    def update(self, instance, validated_data):
        instance = Profile.objects.filter(id=instance.id).update(**validated_data)
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    password = serializers.CharField(write_only=True, min_length=8, max_length=20)
    last_login = serializers.DateTimeField(allow_null=True, required=False)
    is_superuser = serializers.BooleanField(
        help_text='Designates that this user has all permissions without explicitly assigning them.',
        label='Superuser status',
        required=False
    )
    username = serializers.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                     max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(label='Email address', max_length=254, required=False)
    is_staff = serializers.BooleanField(
        help_text='Designates whether the user can log into this admin site.',
        label='Staff status',
        required=False
    )
    is_active = serializers.BooleanField(
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        label='Active', required=False)
    date_joined = serializers.DateTimeField(required=False, write_only=True)
    groups = serializers.PrimaryKeyRelatedField(
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        many=True,
        queryset=Group.objects.all(),
        required=False,
        write_only=True
    )
    group_list = serializers.SerializerMethodField()
    user_permissions = serializers.PrimaryKeyRelatedField(
        help_text='Specific permissions for this user.',
        many=True,
        queryset=Permission.objects.all(),
        required=False
    )
    profile = serializers.SerializerMethodField()

    def get_profile(self, instance):
        profile = get_or_none(Profile, user=instance)
        if isinstance(profile, Profile):
            return {'name': profile.name, 'phone': profile.phone}
        return {'name': None, 'phone': None}

    def get_group_list(self, instance):
        return ','.join(instance.groups.values_list('name', flat=True))

    def validate_username(self, attrs):
        if not validate_username(attrs):
            raise serializers.ValidationError("Not a valid username")
        return attrs

    def validate_password(self, attrs):
        if isinstance(self.instance, User) and attrs:
            raise serializers.ValidationError("Password cannot be changed")

        return attrs

    def to_representation(self, instance):
        self.fields["groups"] = GroupSerializer(many=True, read_only=True)
        self.fields["user_permissions"] = PermissionSerializer(many=True, read_only=True)
        return super().to_representation(instance=instance)

    def create(self, validated_data):
        groups = []
        user_permissions = []

        if "groups" in validated_data.keys():
            groups = validated_data.pop("groups")

        if "user_permissions" in validated_data.keys():
            user_permissions = validated_data.pop("user_permissions")
        instance = User.objects.create_user(**validated_data)

        for group in groups:
            instance.groups.add(group)

        for user_permission in user_permissions:
            instance.user_permissions.add(user_permission)

        return instance

    def update(self, instance, validated_data):
        groups = []
        user_permissions = []

        if "groups" in validated_data.keys():
            instance.groups.clear()
            groups = validated_data.pop("groups")

        if "user_permissions" in validated_data.keys():
            instance.user_permissions.clear()
            user_permissions = validated_data.pop("user_permissions")

        User.objects.filter(id=instance.id).update(**validated_data)

        for group in groups:
            instance.groups.add(group)

        for user_permission in user_permissions:
            instance.user_permissions.add(user_permission)

        return User.objects.get(id=instance.id)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=8, max_length=20, required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset endpoint.
    """
    username = serializers.CharField(max_length=150, required=True, trim_whitespace=True)
    password = serializers.CharField(min_length=8, max_length=20, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    username = serializers.CharField(max_length=150, required=True, trim_whitespace=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class VerifyOTPSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    username = serializers.CharField(max_length=150, required=True, trim_whitespace=True)
    otp = serializers.CharField(max_length=6, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
