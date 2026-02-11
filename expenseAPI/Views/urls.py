from django.urls import path
from Views import views

urlpatterns = [
    path('users/', view=views.all_users),
    path('users/<str:user>/', view=views.specific_user), # 'user' means user's id
    path('users/<str:user>/expenses/', view=views.all_expenses),
    path('users/<str:user>/expenses/<int:expense>/', view=views.specific_expense), # 'expense' means expense's id
    path('users/<str:user>/tokens/', view=views.token) # remind user's token, based on password
]
