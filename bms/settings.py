from pathlib import Path
import os
import dj_database_url
from decouple import config

# BASE_DIR の設定
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = '/Users/skii/Library/CloudStorage/Dropbox/BMS/master'  # 明示的なプロジェクトルート

# SECRET_KEY の取得
SECRET_KEY = config('DJANGO_SECRET_KEY')

# 本番環境判定（環境変数 DJANGO_ENV を使う）
IS_PRODUCTION = os.getenv('DJANGO_ENV') == 'production'

# デバッグモード
DEBUG = not IS_PRODUCTION

# 許可するホスト
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'skm-sk-tokyo-net.herokuapp.com',
]

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
    'attendance',  # 勤怠アプリ
    'accounts',  # アカウント
    'inventory',
    'customers',  # 追加
    'docspdf',
    'core',
    'notifications',
]

# ミドルウェア
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',  # ここを追加
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

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
            ],
        },
    },
]

# メール設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# WSGI設定
WSGI_APPLICATION = 'bms.wsgi.application'

# データベース設定
if IS_PRODUCTION:
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'skm',
            'USER': 'skmaster',
            'PASSWORD': 'sktokyo031114',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 認証設定
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 言語とタイムゾーン
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True
USE_L10N = True

# 静的ファイル設定
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# メディア設定
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ログイン関連
LOGIN_REDIRECT_URL = '/mypage/'
LOGIN_URL = '/login/'

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# logsディレクトリ作成
log_dir = os.path.join(BASE_DIR, 'logs')
os.makedirs(log_dir, exist_ok=True)
