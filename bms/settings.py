from pathlib import Path
import os
import dj_database_url
from decouple import config  # 追加
import cloudinary
import cloudinary.uploader
import cloudinary.api

# BASE_DIR の設定
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY の取得
SECRET_KEY = config('DJANGO_SECRET_KEY')

# DEBUG の設定
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# 許可するホスト
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,skm-sk-tokyo-net.herokuapp.com,skm.sk-tokyo.net,skm-sk-tokyo-net-a3a278cbede9.herokuapp.com').split(',')

# アプリケーション
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_browser_reload',
    'bms',
    'attendance',
    'accounts',
    'inventory',
    'customers',
    'docspdf',
    'core',
    'notifications',
]

# ミドルウェア設定（本番環境のみ WhiteNoise を有効化）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # 本番環境のみ追加

# URL 設定
ROOT_URLCONF = 'bms.urls'

# テンプレート設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bms.context_processors.profile_info',
                'bms.context_processors.company_name',
            ],
        },
    },
]

# WSGI設定
WSGI_APPLICATION = 'bms.wsgi.application'

# データベース設定
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL', default=''))
}

if not DATABASES['default']:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='skm'),
            'USER': config('DB_USER', default='skmaster'),
            'PASSWORD': config('DB_PASSWORD', default='sktokyo031114'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 静的ファイル設定
STATIC_URL = '/static/'

# ローカル（開発環境）では static/ を使用
STATICFILES_DIRS = [BASE_DIR / 'static']

# 本番環境（Heroku）では collectstatic の結果を使用
if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# メディア設定
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ログイン関連
LOGIN_REDIRECT_URL = '/mypage/'
LOGIN_URL = '/login/'

# ロギング設定（エラーのみ記録）
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',  # ERROR 以上のログのみ記録
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),  # ファイル名を変更
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',  # ERROR 以上のログのみ
            'propagate': True,
        },
    },
}

# logsディレクトリ作成
log_dir = BASE_DIR / 'logs'
os.makedirs(log_dir, exist_ok=True)

LANGUAGE_CODE = 'ja'

# メール設定（Xserver SMTP）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sv1416.xserver.jp'  # XserverのSMTPサーバー（契約ごとに異なる）
EMAIL_PORT = 587  # TLSを使用
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # Xserverのメールアドレス
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # メールのパスワード

ADMIN_EXCLUDE_APPS = ["bms", "core", "customers"]

# ここを修正！
DEFAULT_FROM_EMAIL = 'info@sk-tokyo.net'  # 送信元の正しいアドレス
SERVER_EMAIL = 'info@sk-tokyo.net'  # 管理者向けエラー通知も同じアドレスにする


# Cloudinary 設定を `config()` に統一
cloudinary.config( 
  cloud_name = config("CLOUDINARY_CLOUD_NAME", default=""), 
  api_key = config("CLOUDINARY_API_KEY", default=""), 
  api_secret = config("CLOUDINARY_API_SECRET", default="") 
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
