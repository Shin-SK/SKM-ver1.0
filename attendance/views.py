from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import AttendanceRecord, AttendanceStatus, DirectStart
from django.http import HttpResponse
import csv
from django.utils.timezone import now
from django.forms import ModelForm
from django.contrib.auth.models import User
import datetime
from django.utils.dateparse import parse_date  # ← ここを追加！
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


class AttendanceEditForm(ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['clock_in', 'clock_out']

@login_required
def clock_in(request):
    """
    出勤処理

    今ログインしているユーザーの「今日の勤怠データ」を探します。
    なければ新しく作り、出勤時間を記録します。
    終わったらマイページに移動します。
    """
    today = now().date()
    record, created = AttendanceRecord.objects.get_or_create(
        user=request.user, date=today
    )
    if not record.clock_in:
        record.clock_in = now()
        record.save()
    return redirect('mypage')  # リダイレクト先を変更

@login_required
def clock_out(request):
    """
    退勤処理

    今ログインしているユーザーの「今日の勤怠データ」を探します。
    出勤記録が見つかれば、退勤時間を記録します。
    終わったらマイページに移動します。
    """
    today = now().date()
    try:
        record = AttendanceRecord.objects.get(user=request.user, date=today)
        if not record.clock_out:
            record.clock_out = now()
            record.save()
    except AttendanceRecord.DoesNotExist:
        pass  # 出勤記録がない場合は何もしない
    return redirect('mypage')  # リダイレクト先を変更

@login_required
def attendance_dashboard(request):
    """
    勤怠ダッシュボード
    ログイン中のユーザーの勤怠データを一覧表示
    """
    today = now().date()

    # 今日の勤怠記録を取得
    record = AttendanceRecord.objects.filter(user=request.user, date=today).first()

    # 勤怠ステータスを取得（なければ通常勤務として初期化）
    if record:
        attendance_status, created = AttendanceStatus.objects.get_or_create(record=record)
        status = attendance_status.status
    else:
        status = "normal"

    return render(request, 'attendance/attendance_list.html', {
        'records': AttendanceRecord.objects.filter(user=request.user).order_by('-date'),
        'attendance_status': status,  # ← フロントエンドに渡す
    })



@user_passes_test(lambda u: u.is_staff)
def admin_attendance_list(request):
    """
    管理者向け: 全社員の勤怠データリスト（フィルタリング対応）

    フィルタリング条件:
    - 月ごと (month)
    - 年ごと (year)
    - 名前ごと (name)
    - 全員
    """
    records = AttendanceRecord.objects.select_related('user').order_by('-date')

    # 現在の日時をコンテキストに追加
    current_time = now()

    # フィルタリング条件を取得
    month = request.GET.get('month')
    year = request.GET.get('year')
    name = request.GET.get('name')

    # 名前でフィルタリング
    if name:
        records = records.filter(user__username__icontains=name)

    # 月・年でフィルタリング
    if year:
        records = records.filter(date__year=year)
    if month:
        records = records.filter(date__month=month)

    # 月の選択肢を生成
    months = range(1, 13)

    # 全ユーザーのリストを取得
    users = User.objects.all()

    return render(request, 'attendance/admin_list.html', {
        'records': records,
        'month': month,
        'year': year,
        'name': name,
        'now': current_time,
        'months': months,  # これを追加
        'users': users,
    })

@user_passes_test(lambda u: u.is_staff)
def export_attendance_csv(request):
    """
    勤怠データのCSVエクスポート

    管理者は全ての社員の勤怠データをCSVファイルに保存してダウンロードできます。
    """
    records = AttendanceRecord.objects.select_related('user').order_by('date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Date', 'Clock In', 'Clock Out'])
    for record in records:
        writer.writerow([
            record.user.username,
            record.date,
            record.clock_in,
            record.clock_out
        ])

    return response

@user_passes_test(lambda u: u.is_staff)
def edit_attendance(request, record_id):
    """
    勤怠データの編集ページ
    管理者が出勤時間・退勤時間を編集できます。
    """
    record = get_object_or_404(AttendanceRecord, id=record_id)
    if request.method == 'POST':
        form = AttendanceEditForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('admin_attendance_list')
    else:
        form = AttendanceEditForm(instance=record)
    return render(request, 'attendance/edit_attendance.html', {'form': form, 'record': record})


@login_required
def set_direct_start(request):
    if request.method == "POST":
        date_str = request.POST.get("date")

        # デバッグ用ログ
        print(f"受け取った日付（文字列）: {date_str}")

        date = parse_date(date_str)  # 文字列を日付型に変換

        print(f"変換後の日付（Date型）: {date}")  # デバッグ用

        if date:
            obj, created = DirectStart.objects.update_or_create(
                user=request.user, date=date, defaults={"is_direct_start": True}
            )
            print(f"直行予約を{'作成' if created else '更新'}しました: {obj}")  # デバッグ用
        else:
            print("日付が正常に変換されなかったため、保存されませんでした。")

    return redirect('mypage')



@login_required
def delete_direct_start(request, direct_start_id):
    """
    直行予約を削除する（JSなしで動くように変更）
    """
    direct_start = get_object_or_404(DirectStart, id=direct_start_id, user=request.user)
    direct_start.delete()
    return redirect('mypage')  # 🔥 削除後はマイページへリダイレクト！




@login_required
def set_attendance_status(request):
    """
    勤怠ステータスを設定（午前休・午後休）
    """
    if request.method == "POST":
        status = request.POST.get("attendance_status")
        today = now().date()

        record, created = AttendanceRecord.objects.get_or_create(user=request.user, date=today)

        if record:
            attendance_status, created = AttendanceStatus.objects.get_or_create(record=record)
            attendance_status.status = status
            attendance_status.save()
        else:
            pass  # ログを記録しないので、何もしない

    return redirect('mypage')
