from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from attendance.models import AttendanceRecord
from .models import Employee
from .forms import EmployeeForm
import logging
import csv
from django.http import HttpResponse
from .utils import get_employee_by_user
from notifications.models import Notification
from .models import Employee

logger = logging.getLogger('django')

# 操作者を設定するミックスイン（未使用のため一旦削除）

# 編集ビュー
@user_passes_test(lambda u: u.is_staff)
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)
            instance._current_user = request.user  # 操作者をセット
            instance.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'bms/edit_employee.html', {'form': form, 'employee': employee})

# 削除ビュー
@user_passes_test(lambda u: u.is_staff)
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    logger.info(f"User: {request.user} deleted Employee ID={employee.id}")
    employee.delete()
    return redirect('employee_list')


# 社員リストビュー
@user_passes_test(lambda u: u.is_staff)
def employee_list(request):
    search_name = request.GET.get('name', '')
    search_department = request.GET.get('department', '')
    search_employee_number = request.GET.get('employee_number', '')

    employees = Employee.objects.all()
    if search_name:
        employees = employees.filter(first_name__icontains=search_name)
    if search_department:
        employees = employees.filter(department__icontains=search_department)
    if search_employee_number:
        employees = employees.filter(employee_number=search_employee_number)

    return render(request, 'bms/employee_list.html', {
        'employees': employees,
        'search_name': search_name,
        'search_department': search_department,
        'search_employee_number': search_employee_number,
    })

    search_name = request.GET.get('name', '')
    search_department = request.GET.get('department', '')

    employees = Employee.objects.all()
    if search_name:
        employees = employees.filter(first_name__icontains=search_name)
    if search_department:
        employees = employees.filter(department__icontains=search_department)

    return render(request, 'bms/employee_list.html', {
        'employees': employees,
        'search_name': search_name,
        'search_department': search_department,
    })

# CSVダウンロードビュー
@user_passes_test(lambda u: u.is_staff)
def export_employees_csv(request):
    search_name = request.GET.get('name', '')
    search_department = request.GET.get('department', '')

    employees = Employee.objects.all()
    if search_name:
        employees = employees.filter(first_name__icontains=search_name)
    if search_department:
        employees = employees.filter(department__icontains=search_department)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['名', '姓', '部署', 'メールアドレス', '電話番号'])
    for employee in employees:
        writer.writerow([
            employee.first_name or '',
            employee.last_name or '',
            employee.department or '',
            employee.email or '',
            employee.phone_number or '',
        ])

    return response

# マイページビュー
@login_required
def mypage(request):
    user = request.user

    # プロフィール情報を作成（デフォルト値込み）
    profile_info = {
        '姓': user.first_name or '設定されていません',
        '名': user.last_name or '設定されていません',
        'ログインID': user.username or '設定されていません',
        'メールアドレス': user.email or '設定されていません',
        '電話番号': getattr(user, 'profile', None) and getattr(user.profile, 'phone_number', '設定されていません'),
        '部署': getattr(user, 'profile', None) and getattr(user.profile, 'department', '設定されていません'),
    }

    # Employee（社員情報）を取得（なければダミーをセット）
    employee = Employee.objects.filter(email=user.email).first()
    if not employee:
        employee = Employee(employee_number="000000", email=user.email)  # ダミーデータ

    # 今日の勤怠情報を取得
    today = now().date()
    record = AttendanceRecord.objects.filter(user=user, date=today).first()

    # 通知データを取得（最新5件）
    notifications = Notification.objects.filter(notification_type='全体').order_by('-created_at')[:5]

    # テンプレートに渡す
    return render(request, 'bms/mypage.html', {
        'profile_info': profile_info,
        'employee': employee,
        'record': record,
        'notifications': notifications,
    })

# 出勤ビュー
@login_required
def clock_in(request):
    today = now().date()
    record, created = AttendanceRecord.objects.get_or_create(
        user=request.user, date=today
    )
    if not record.clock_in:
        record.clock_in = now()
        record.save()
    return redirect('mypage')

# 退勤ビュー
@login_required
def clock_out(request):
    today = now().date()
    try:
        record = AttendanceRecord.objects.get(user=request.user, date=today)
        if not record.clock_out:
            record.clock_out = now()
            record.save()
    except AttendanceRecord.DoesNotExist:
        pass
    return redirect('mypage')


def index(request):
    # ユーザーがログインしている場合はマイページへリダイレクト
    if request.user.is_authenticated:
        return redirect('/mypage/')
    # 未ログインの場合はログインページへリダイレクト
    return redirect('/login/')

def employee_detail(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})


    from django.shortcuts import render

def preview_error(request, error_code=404):
    error_messages = {
        400: ("不正なリクエスト", "申し訳ありません。リクエストに問題があります。"),
        403: ("アクセス拒否", "申し訳ありません。このページにアクセスする権限がありません。"),
        404: ("ページが見つかりません", "申し訳ありません。お探しのページは存在しないか、移動した可能性があります。"),
        500: ("サーバーエラー", "申し訳ありません。サーバー内部で問題が発生しました。しばらくしてから再度お試しください。"),
    }
    
    title, message = error_messages.get(error_code, ("エラー", "予期しないエラーが発生しました。"))
    
    return render(request, "error.html", {
        "error_code": error_code,
        "error_title": title,
        "error_message": message,
    }, status=error_code)
