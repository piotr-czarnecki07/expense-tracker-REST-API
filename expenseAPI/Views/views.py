from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from DB.models import User
from Views.serializers import UserSerializer

from Views.hash import hash_table, dehash_table, CHARACTERS
import random

def hash_text(text: str) -> str:
    hashed = ''
    for c in text:
        hashed += hash_table[c]
    return hashed

def dehash_text(text: str) -> str:
    dehashed = ''
    for c in text:
        dehashed += dehash_table[c]
    return dehashed

@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET': # return a list of all users
        try:
            users = User.objects.all() # Queryset of all users
            serializer = UserSerializer(users, many=True)

        except DatabaseError as e:
            return Response({'error': f'Database is not available: {e}'}, st.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.data, st.HTTP_200_OK)

    else: # POST method; add a new user
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except KeyError as e:
            return Response({'error': f'Parameter {e} was not provided'}, st.HTTP_400_BAD_REQUEST)

        # parameters validation
        if User.objects.filter(username=username).first() is not None:
            return Response({'error': 'This username already exists'}, st.HTTP_409_CONFLICT)

        if User.objects.filter(email=email).first() is not None:
            return Response({'error': 'This email is already in use'}, st.HTTP_409_CONFLICT)

        if '@' not in email or '.' not in email:
            return Response({'error': 'Email is invalid'}, st.HTTP_400_BAD_REQUEST)

        token = ''
        for _ in range(50):
            token += CHARACTERS[random.randint(0, 43)]

        try:
            user = User(username=username, email=email, password=hash_text(password), token=hash_text(token))
            user.save()

        except ValidationError as e:
            return Response({'error': f'User data is invalid, {e}'}, st.HTTP_400_BAD_REQUEST)
        
        except DatabaseError as e:
            return Response({'error': f'Database is not available: {e}'}, st.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data, st.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_user(request, user: int):
    pass

@api_view(['GET', 'POST'])
def all_expenses(request, user: int):
    pass

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_expense(request, user: int, expense: int):
    pass
