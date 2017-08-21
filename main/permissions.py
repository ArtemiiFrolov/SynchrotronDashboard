from main.models import SpecialPermissionsMixin


class ObjectPermissionsBackend(object):
    def has_perm(self, user, perm, obj=None):
        if obj is None:
            return False

        if not isinstance(obj, SpecialPermissionsMixin):
            return False

        if obj.special_user_permissions.filter(user=user, permission__codename=perm).exists():
            return True

        return False


    def has_module_perms(self, user, app_label):
        return app_label == 'main'
