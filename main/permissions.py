from main.models import SpecialPermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

UserModel = get_user_model()


class ObjectPermissionsBackend(object):
    def has_perm(self, user, perm, obj=None):
        if obj is None:
            return False

        if not isinstance(obj, SpecialPermissionsMixin):
            return False

        user_perms = set()
        for special_perm in obj.special_user_permissions.all():
            user_perms.add((special_perm.user.pk, special_perm.permission_label))

        group_perms = set()
        for special_perm in obj.special_group_permissions.all():
            group_perms.add((special_perm.group.pk, special_perm.permission_label))

        if (user.pk, perm) in user_perms:
            return True

        for group in user.groups.all():
            if (group.pk, perm) in group_perms:
                return True

        return False


    def has_module_perms(self, user, app_label):
        #return True
        return app_label == 'main'
