from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "scarlet.pagebuilder"

    def ready(self):
        super().ready()
        self.module.autodiscover()
