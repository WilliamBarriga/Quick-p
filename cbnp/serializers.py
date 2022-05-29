from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework.serializers import (
    Serializer,
    CharField,
    EmailField,
    IntegerField,
    FileField,
    BooleanField,
    JSONField,
    ModelSerializer,
    ValidationError,
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['name'] = user.name
        return token


class SignInSerializer(ModelSerializer):
    email = EmailField(required=True)
    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    password_confirmation = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'email', ]

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise ValidationError({"password": "Passwords don't match"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.set_password(validated_data['password'])
        return user


class ClientSerializer(Serializer):
    """
    ClientsSerializer
    """
    id = IntegerField(read_only=True)
    document = IntegerField(required=True, max_value=99999999999)
    first_name = CharField(required=True, max_length=50)
    last_name = CharField(required=True, max_length=50)
    email = EmailField(required=True, max_length=50)


class ProductSerializer(Serializer):
    """
    ProductsSerializer
    """
    id = IntegerField(read_only=True)
    is_active = BooleanField(read_only=True)
    name = CharField(required=True, max_length=50)
    description = CharField(required=True, max_length=255)
    attributes = JSONField()


class FileSerializer(Serializer):
    """
    FileSerializer
    """
    file = FileField(required=True)
