from django.apps import AppConfig

class FrameworksProjectUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frameworks_project_users'

    def ready(self):
        import frameworks_project_users.signals
