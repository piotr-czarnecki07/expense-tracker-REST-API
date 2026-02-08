from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as st

@api_view(['GET', 'POST'])
def all_users(request):
    pass

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_user(request, user: int):
    pass

@api_view(['GET', 'POST'])
def all_expenses(request, user: int):
    pass

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def specific_expense(request, user: int, expense: int):
    pass
