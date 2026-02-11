from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from DB.models import User, Expense
from Views.serializers import UserSerializer, UserBulkSerializer, ExpenseSerializer, ExpenseBulkSerializer

from Views.hash import hash_table, dehash_table, CHARACTERS

from functools import wraps
import random

def hash_text(text: str) -> str:
    hashed = ''
    for c in text:
        hashed += hash_table[c]
    return hashed

# syntactic sugar functions
def db_error(e):
    return Response({'error': f'Database is not available: {e}'}, st.HTTP_500_INTERNAL_SERVER_ERROR)

def key_error(e):
    return Response({'error': f'Parameter {e} was not provided'}, st.HTTP_400_BAD_REQUEST)

def amount_type_error(e):
    return Response({'error': f"Parameter 'amount' is of wrong type: {e}"}, st.HTTP_400_BAD_REQUEST)

# decorators
def find_user(view):
    @wraps(view)
    def wrapper(request, *args):
        try:
            user_obj = User.objects.filter(username=args[0]).first()
            if user_obj is None:
                return Response({'error': f"Username '{args[0]}' not found"}, st.HTTP_404_NOT_FOUND)

        except DatabaseError as db_e:
            return db_error(db_e)

        request.user_obj = user_obj

        return view(request, *args)

    return wrapper

def get_token(view):
    @wraps(view)
    def wrapper(request, *args):
        try:
            token = request.data['token']

        except KeyError:
            token = request.query_params.get('token') # for GET and DELETE methods, token must be in query parameters
                                                      # otherwise it can be placed within request body
            if token is None:
                return Response({'error': 'User token was not provided'}, st.HTTP_403_FORBIDDEN)

        request.token = token

        return view(request, *args)

    return wrapper


@api_view(['GET', 'POST'])
def all_users(request):
    if request.method == 'GET': # return a list of all users
        try:
            users = User.objects.all() # Queryset of all users
            serializer = UserBulkSerializer(users, many=True)

        except DatabaseError as db_e:
            return db_error(db_e)
        
        except AttributeError as atr_e:
            return Response({'error': f"Data of this user had been deleted"}, st.HTTP_410_GONE)

        else:
            return Response(serializer.data, st.HTTP_200_OK)

    else: # POST method; add a new user
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except KeyError as key_e:
            return key_error(key_e)

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
@find_user
@get_token
def specific_user(request, user: str):
    # validate token
    if request.user_obj.token != hash_text(request.token):
        return Response({'error': f"Token '{request.token}' is invalid"}, st.HTTP_401_UNAUTHORIZED)

    # perform operations
    if request.method == 'GET':
        serializer = UserSerializer(request.user_obj)
        return Response(serializer.data, st.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

        except KeyError as key_e:
            return key_error(key_e)

        try:
            request.user_obj.username = username
            request.user_obj.email= email
            request.user_obj.password = hash_text(password)
            request.user_obj.save()

        except ValidationError as val_e:
            return Response({'error': f'User data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            serializer = UserSerializer(request.user_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    elif request.method == 'PATCH':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            if username is not None:
                request.user_obj.username = username

            if email is not None:
                request.user_obj.email = email

            if password is not None:
                request.user_obj.password = hash_text(password)

            request.user_obj.save()

        except ValidationError as val_e:
            return Response({'error': f'User data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            serializer = UserSerializer(request.user_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    else: # DELETE
        try:
            serializer = UserSerializer(request.user_obj)
            request.user_obj.delete()

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            return Response(serializer.data, st.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@find_user
@get_token
def all_expenses(request, user: str):
    # validate token
    if request.user_obj.token != hash_text(request.token):
        return Response({'error': f"Token '{request.token}' is invalid"}, st.HTTP_401_UNAUTHORIZED)

    # perform operations
    if request.method == 'GET':
        try:
            expenses = [Expense.objects.filter(id=expense_id).first() for expense_id in request.user_obj.expense_ids]
            serializer = ExpenseBulkSerializer(expenses, many=True)

        except DatabaseError as db_e:
            return db_error(db_e)
        
        except AttributeError as atr_e:
            return Response({'error': f"Data of this expense had been deleted"}, st.HTTP_410_GONE)

        else:
            return Response(serializer.data, st.HTTP_200_OK)

    else: # POST; adds a new expense
        try:
            title = request.data['title']
            amount = float(request.data['amount'])
            category = request.data['category']

            expense = Expense(title=title, amount=amount, category=category)
            expense.save()

            request.user_obj.expense_ids.append(expense.id)
            request.user_obj.save()

        except (KeyError, TypeError) as key_e: # TypeError means that amount parameter was not provided
            return key_error(key_e)

        except ValueError as v_e:
            return amount_type_error(v_e)

        except ValidationError as val_e:
            return Response({'error': f'Expense data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)

        else:
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data, st.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@find_user
@get_token
def specific_expense(request, user: str, expense: int):
    # validate token
    if request.user_obj.token != hash_text(request.token):
        return Response({'error': f"Token '{request.token}' is invalid"}, st.HTTP_401_UNAUTHORIZED)

    try:    
        expense_obj = Expense.objects.filter(id=expense).first()
        if expense_obj is None:
            return Response({'error': f"Expense with an id '{expense}' was not found"}, st.HTTP_404_NOT_FOUND)

    except DatabaseError as db_e:
        return db_error(db_e)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense_obj)
        return Response(serializer.data, st.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            expense_obj.title = request.data['title']
            expense_obj.amount = float(request.data['amount'])
            expense_obj.category = request.data['category']
            expense_obj.save()

        except (KeyError, TypeError) as key_e: # TypeError means that amount parameter was not provided
            return key_error(key_e)

        except ValueError as v_e:
            return amount_type_error(v_e)

        except ValidationError as val_e:
            return Response({'error': f'Expense data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)
        
        else:
            serializer = ExpenseSerializer(expense_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    elif request.method == 'PATCH':
        try:
            title = request.data.get('title')
            amount = request.data.get('amount')
            category = request.data.get('category')

            if title is not None:
                expense_obj.title = title

            if amount is not None:
                expense_obj.amount = float(amount)

            if category is not None:
                expense_obj.category = category

            expense_obj.save()

        except ValueError as v_e:
            return amount_type_error(v_e)

        except ValidationError as val_e:
            return Response({'error': f'Expense data is invalid, {val_e}'}, st.HTTP_400_BAD_REQUEST)

        except DatabaseError as db_e:
            return db_error(db_e)
        
        else:
            serializer = ExpenseSerializer(expense_obj)
            return Response(serializer.data, st.HTTP_205_RESET_CONTENT)

    else: # DELETE
        try:
            id_to_remove = expense_obj.id

            serializer = ExpenseSerializer(expense_obj)
            expense_obj.delete()

            request.user_obj.expense_ids.remove(id_to_remove)
            request.user_obj.save()

        except DatabaseError as db_e:
            return db_error(db_e)
        
        else:
            return Response(serializer.data, st.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@find_user
def token(request, user: str):
    # validate password
    password = request.query_params.get('password')
    if password is None:
        return Response({'error': 'Password was not provided'}, st.HTTP_403_FORBIDDEN)

    if request.user_obj.password != hash_text(password):
        return Response({'error': f"Password '{password}' is invalid"}, st.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET': # remind token
        token = ''
        for c in request.user_obj.token:
            token += dehash_table[c]

        return Response({'token': token}, st.HTTP_200_OK)
