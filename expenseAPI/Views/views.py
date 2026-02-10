from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from DB.models import User, Expense
from Views.serializers import UserSerializer, ExpenseSerializer, ExpenseBulkSerializer

from Views.hash import hash_table, CHARACTERS
import random

def hash_text(text: str) -> str:
    hashed = ''
    for c in text:
        hashed += hash_table[c]
    return hashed

def db_error(e): # function for less verbose syntax
    return Response({'error': f'Database is not available: {e}'}, st.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET': # return a list of all users
        try:
            users = User.objects.all() # Queryset of all users
            serializer = UserSerializer(users, many=True)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            return Response(serializer.data, st.HTTP_200_OK)

    else: # POST method; add a new user
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except KeyError as key_e:
            return Response({'error': f'Parameter {key_e} was not provided'}, st.HTTP_400_BAD_REQUEST)

        # parameters validation
        if User.objects.filter(username=username).first() is not None:
            return Response({'error': 'This username already exists'}, st.HTTP_409_CONFLICT)

        if User.objects.filter(email=email).first() is not None:
            return Response({'error': 'This email is already in use'}, st.HTTP_409_CONFLICT)

        if '@' not in email or '.' not in email:
            return Response({'error': 'Email is invalid'}, st.HTTP_400_BAD_REQUEST)

        token = ''
        for _ in range(50):
            token += CHARACTERS[random.randint(0, 38)]

        try:
            user = User(username=username, email=email, password=hash_text(password), token=hash_text(token))
            user.save()

        except KeyError:
            return Response({'error': 'Password must contain ONLY the following characters: a-z  0-9  !@#$^&*  _-'}, st.HTTP_400_BAD_REQUEST)

        except ValidationError as val_e:
            return Response({'error': f'User data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)
        
        except DatabaseError as db_e:
            return db_error(db_e)
        
        else:
            return Response({'token': token}, st.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_user(request, user: str):
    # find user
    try:
        user_obj = User.objects.filter(username=user).first()
        if user_obj is None:
            return Response({'error', f"Username '{user}' not found"}, st.HTTP_404_NOT_FOUND)
        
    except DatabaseError as db_e:
        return db_error(db_e)

    # validate token
    try:
        token = request.data['token']

    except KeyError as key_e:
        token = request.query_params.get('token') # for GET and DELETE methods, token must be in query parameters
                                                  # otherwise it can be placed within request body
        if token is None:
            return Response({'error': f'User token was not provided: {key_e}'}, st.HTTP_400_BAD_REQUEST)

    if user_obj.token != hash_text(token):
        return Response({'error': f"Token '{token}' is invalid"}, st.HTTP_401_UNAUTHORIZED)

    # perform operations
    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return Response(serializer.data, st.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except KeyError as key_e:
            return Response({'error': f'Parameter {key_e} was not provided'}, st.HTTP_400_BAD_REQUEST)

        try:
            user_obj.username = username
            user_obj.email= email
            user_obj.password = hash_text(password)
            user_obj.save()

        except ValidationError as val_e:
            return Response({'error': f'User data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            serializer = UserSerializer(user_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    elif request.method == 'PATCH':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            if username is not None:
                user_obj.username = username

            if email is not None:
                user_obj.email = email

            if password is not None:
                user_obj.password = hash_text(password)

            user_obj.save()

        except ValidationError as val_e:
            return Response({'error': f'User data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            serializer = UserSerializer(user_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    else: # DELETE
        try:
            serializer = UserSerializer(user_obj)
            user_obj.delete()

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            return Response(serializer.data, st.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def all_expenses(request, user: str):
    # find user
    try:
        user_obj = User.objects.filter(username=user).first()
        if user_obj is None:
            return Response({'error', f"Username '{user}' not found"}, st.HTTP_404_NOT_FOUND)
        
    except DatabaseError as db_e:
        return db_error(db_e)

    # validate token
    try:
        token = request.data['token']

    except KeyError as key_e:
        token = request.query_params.get('token') # for GET and DELETE methods, token must be in query parameters
                                                  # otherwise it can be placed within request body
        if token is None:
            return Response({'error': f'User token was not provided: {key_e}'}, st.HTTP_400_BAD_REQUEST)

    if user_obj.token != hash_text(token):
        return Response({'error': f"Token '{token}' is invalid"}, st.HTTP_401_UNAUTHORIZED)
    
    # perform operations
    if request.method == 'GET':
        try:
            expenses = Expense.objects.all()

        except DatabaseError as db_e:
            return db_error(db_e)
        
        else:
            serializer = ExpenseBulkSerializer(expenses, many=True)
            return Response(serializer.data, st.HTTP_200_OK)
        
    else:
        pass


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_expense(request, user: str, expense: int):
    pass
