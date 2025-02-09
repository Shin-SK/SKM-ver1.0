from .models import Employee

def get_employee_by_user(user):
    """
    ログインユーザーに紐づくEmployee情報を取得
    """
    return Employee.objects.filter(email=user.email).first()
