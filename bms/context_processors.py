from django.contrib.auth.models import User
from bms.models import Employee

def profile_info(request):
    if request.user.is_authenticated:
        user = request.user
        employee = Employee.objects.filter(email=user.email).first()

        # employee がない場合、ダミーデータを設定
        if not employee:
            employee = Employee(employee_number="000000", email=user.email)

        return {
            'profile_info': {
                '姓': user.first_name or '設定されていません',
                '名': user.last_name or '設定されていません',
                'ログインID': user.username or '設定されていません',
                'メールアドレス': user.email or '設定されていません',
                '電話番号': getattr(user, 'profile', None) and getattr(user.profile, 'phone_number', '設定されていません'),
                '部署': getattr(user, 'profile', None) and getattr(user.profile, 'department', '設定されていません'),
            },
            'employee': employee  # Employeeデータも全ページで使えるようにする
        }
    return {'profile_info': None, 'employee': None}
