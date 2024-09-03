# create_roles.py in one of your app's management/commands directory

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from models import Role  # Import your Role model

class Command(BaseCommand):
    help = 'Create default user roles'

    def handle(self, *args, **kwargs):
        roles_permissions = {
            'Admin': ['change_user', 'view_user'],  # Admin can change and view users
            'Editor': ['add_post', 'change_post', 'delete_post', 'view_post'],  # Example permissions for Editor
            'Viewer': ['view_post'],  # Example permissions for Viewer
        }

        for role_name, permissions in roles_permissions.items():
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created.'))

            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    role.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm}" not found.'))

            self.stdout.write(self.style.SUCCESS(f'Permissions for role "{role_name}" set up.'))
