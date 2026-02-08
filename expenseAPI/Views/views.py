from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

from django.core.exceptions import ValidationError
from django.db import DatabaseError

from DB.models import User
from Views.serializers import UserSerializer

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

    elif request.method == 'POST': # add a new user
        pass

    else:
        return Response({'error': 'Invalid HTTP method'}, st.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_user(request, user: int):
    pass

@api_view(['GET', 'POST'])
def all_expenses(request, user: int):
    pass

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_expense(request, user: int, expense: int):
    pass
