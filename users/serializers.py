from rest_framework import serializers
from .models import User
from roles.models import Role
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

"""
    @AUTHOR: Ivan Sanchez
    @LAST_UPDATE: 2026-09-19
    @DESCRIPTION: Serializadores para gestión de usuarios y autenticación personalizada JWT.
"""
#* Serializadores para gestión de usuarios y autenticación personalizada JWT.
class RoleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

#* Serializador para el modelo User.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=False, 
        style={'input_type': 'password'}
    )
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), 
        many=True, 
        required=False
    )
    roles_detail = RoleSimpleSerializer(source='roles', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'birth_date', 
            'phone_number', 
            'is_active', 
            'roles',          
            'roles_detail',  
            'password', 
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        if 'username' not in validated_data or not validated_data['username']:
            validated_data['username'] = validated_data.get('email')
        
        user = User.objects.create_user(password=password, **validated_data)
        
        if self.context.get('registration'):
            user.roles.add(Role.objects.get(pk=1))
        elif roles_data:
            user.roles.set(roles_data)
        else:
            default_role, _ = Role.objects.get_or_create(name='Lector')
            user.roles.add(default_role)
            
        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if roles_data is not None:
            instance.roles.set(roles_data)

        return instance

#* Serializador personalizado para la obtención de tokens JWT que incluye información adicional del usuario.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['roles'] = list(user.roles.values_list('name', flat=True))

        return token

    def validate(self, attrs):
        email = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Debe incluir 'email' y 'password'."}
            )

        user = authenticate(
            request=self.context.get('request'),
            username=email, 
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": "No existe una cuenta activa con las credenciales proporcionadas."}
            )

        credentials = {
            self.username_field: user.email,
            "password": password
        }

        data = super().validate(credentials)
        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data

        return data