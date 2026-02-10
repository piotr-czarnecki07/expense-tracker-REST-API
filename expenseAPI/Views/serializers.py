from rest_framework.serializers import ModelSerializer
from DB.models import User, Expense

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'created_at', 'expense_ids']

class UserBulkSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseBulkSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['title', 'amount']
