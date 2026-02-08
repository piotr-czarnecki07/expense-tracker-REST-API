from django.urls import path
from Views import views

urlpatterns = [
    path('users/', view=views.all_users),
    path('users/<int:user>/', view=views.specific_user), # 'user' means user's id
    path('users/<int:user>/expenses/', view=views.all_expenses),
    path('users/<int:user>/expenses/<int:expense>/', view=views.specific_expense) # 'expense' means expense's id
]
