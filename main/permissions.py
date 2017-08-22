from main.models import SpecialPermissionsMixin
from django.contrib.auth.backends import ModelBackend


class ObjectPermissionsBackend(ModelBackend):
    def has_perm(self, user, perm, obj=None):
        basic = ModelBackend.has_perm(self, user, perm)
        if basic:
            return True

        # if basic perm checking fails
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
        if app_label == 'main':
            return True
        return ModelBackend.has_module_perms(self, user, app_label)



