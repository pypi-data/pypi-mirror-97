import os

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))


TEST_APPS = [
    file.name
    for file in os.scandir(TESTS_DIR)
    if os.path.isdir(os.path.join(TESTS_DIR, file.name))
    and "." not in file.name
    and not file.name.startswith("__")
]


DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]

SCARLET_AND_OTHER_APPS = [
    "scarlet.cms",
    "scarlet.assets",
    "scarlet.accounts",
    "scarlet.versioning",
    "scarlet.scheduling",
    "scarlet.pagebuilder",
    "taggit",
    "webpack_loader",
]

urls = "cms_bundles.urls"


SECRET_KEY = "Please do not spew DeprecationWarnings"
SITE_ID = 1
INSTALLED_APPS = DJANGO_APPS + SCARLET_AND_OTHER_APPS + TEST_APPS
STATIC_URL = "static/"
ROOT_URLCONF = urls
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "scarlet.versioning.postgres_backend",
        "NAME": "scarlet",
        "USER": "scarlet",
        "PASSWORD": "scarlet",
        "HOST": "localhost",
        "PORT": "",
    },
}
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            "debug": True,
        },
    },
]
