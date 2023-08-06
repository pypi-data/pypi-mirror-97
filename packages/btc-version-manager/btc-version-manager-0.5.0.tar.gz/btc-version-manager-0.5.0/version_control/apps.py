from django.apps import AppConfig


class VersionControlConfig(AppConfig):
    name = 'version_control'
    verbose_name = 'Контроль версий'

    def ready(self):
        import version_control.signals
