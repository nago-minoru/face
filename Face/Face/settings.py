import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$v18(@al8@x#@j%k-l7x!=b^ska2$4&(j6dnfi-gypxek7a)35'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Debug Toolbar
# if DEBUG:
#     INTERNAL_IPS = ['127.0.0.1', 'localhost']
#
#     def custom_show_toolbar(request):
#         return True
#
#     DEBUG_TOOLBAR_PANELS = [
#         'debug_toolbar.panels.timer.TimerPanel',
#         'debug_toolbar.panels.request.RequestPanel',
#         'debug_toolbar.panels.sql.SQLPanel',
#         'debug_toolbar.panels.templates.TemplatesPanel',
#         'debug_toolbar.panels.cache.CachePanel',
#         'debug_toolbar.panels.logging.LoggingPanel',
#     ]
#
#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#         'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
#         'HIDE_DJANGO_SQL': False,
#         'TAG': 'div',
#         'ENABLE_STACKTRACES': True,
#     }

# 公開用の設定
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # セッションある
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',     # ブートストラップ
    'FaceShoot',      # 自作アプリ
    'widget_tweaks',  # ログイン間緑化
    'django_cleanup', # 削除時の残滓を消去
    'debug_toolbar',  # デバッグ
    'stdimage',       # 画像サイズ変更

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # セッション(デフォ)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # デバッグ用に追加

]

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # 追加
    'django.contrib.sessions.middleware.SessionMiddleware'  # セッション
]

# セッションは自力で有効化する
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'  # ファイル単位
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # キャッシュ単位
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # 永続キャッシュ
# SESSION_FILE_PATH = #ファイルで保存する場合はパスを指定 デフォルト値==tempfile.gettempdir()
# SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies" #クッキー単位

ROOT_URLCONF = 'Face.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'media/'),
                 os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],  # プロジェクト単位
        # 'DIRS': [os.path.join(BASE_DIR, 'FaceShootFace/templates')],  # アプリ単位
        # 'DIRS': [os.path.join(BASE_DIR, 'media/')], # 画像フォルダ
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
TEMPLATE_DIRS = ('templates/',)

WSGI_APPLICATION = 'Face.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = False
# MySQLの日付型の対応をするために変更
# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'FaceShoot/static/'),
)

# アップロードフォルダのパス
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# アップロード先フォルダ
MEDIA_URL = '/media/'






